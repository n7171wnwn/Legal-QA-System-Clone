#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将案例数据从 legal_articles 表迁移到 legal_cases 表
"""

import pymysql
import re
from datetime import datetime

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'hjj060618',
    'database': 'legal_qa',
    'charset': 'utf8mb4'
}

def extract_case_info(content):
    """从案例内容中提取信息"""
    case_type = None
    court_name = None
    judge_date = None
    dispute_point = None
    judgment_result = None
    
    if not content:
        return case_type, court_name, judge_date, dispute_point, judgment_result
    
    # 提取案由
    case_type_patterns = [
        r'案由[：:]\s*(.+?)(?:\n|$)',
        r'案件类型[：:]\s*(.+?)(?:\n|$)',
    ]
    for pattern in case_type_patterns:
        match = re.search(pattern, content)
        if match:
            case_type = match.group(1).strip()
            break
    
    # 提取审理法院
    court_patterns = [
        r'审理法院[：:]\s*(.+?)(?:\n|$)',
        r'法院[：:]\s*(.+?)(?:\n|$)',
        r'(.+?法院)',
    ]
    for pattern in court_patterns:
        match = re.search(pattern, content)
        if match:
            court_name = match.group(1).strip()
            if len(court_name) < 50:  # 避免匹配到太长的内容
                break
    
    # 提取判决日期
    date_patterns = [
        r'判决日期[：:]\s*(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?)',
        r'(\d{4})年(\d{1,2})月(\d{1,2})日',
        r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})',
    ]
    for pattern in date_patterns:
        match = re.search(pattern, content)
        if match:
            if len(match.groups()) == 3:
                year, month, day = match.groups()
                date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            else:
                date_str = match.group(1).replace('年', '-').replace('月', '-').replace('日', '')
                date_str = re.sub(r'[年月日]', '-', date_str).strip('-')
                parts = date_str.split('-')
                if len(parts) >= 3:
                    date_str = f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
            
            try:
                judge_date = datetime.strptime(date_str, '%Y-%m-%d')
            except:
                try:
                    judge_date = datetime.strptime(date_str, '%Y-%m')
                except:
                    pass
            if judge_date:
                break
    
    # 提取核心争议点
    dispute_patterns = [
        r'争议点[：:]\s*(.+?)(?:\n\n|$)',
        r'核心争议[：:]\s*(.+?)(?:\n\n|$)',
        r'争议焦点[：:]\s*(.+?)(?:\n\n|$)',
    ]
    for pattern in dispute_patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            dispute_point = match.group(1).strip()[:2000]  # 限制长度
            break
    
    # 提取判决结果
    result_patterns = [
        r'判决结果[：:]\s*(.+?)(?:\n\n|$)',
        r'判决[：:]\s*(.+?)(?:\n\n|$)',
        r'裁判结果[：:]\s*(.+?)(?:\n\n|$)',
    ]
    for pattern in result_patterns:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            judgment_result = match.group(1).strip()[:2000]  # 限制长度
            break
    
    return case_type, court_name, judge_date, dispute_point, judgment_result

def migrate_cases():
    """迁移案例数据"""
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    
    print("=" * 70)
    print("将案例数据从 legal_articles 迁移到 legal_cases")
    print("=" * 70)
    
    try:
        # 步骤1: 查找所有案例
        print("\n【步骤1】查找案例数据...")
        cursor.execute("""
            SELECT id, title, content, law_type, create_time
            FROM legal_articles
            WHERE law_type = '案例'
        """)
        
        cases = cursor.fetchall()
        print(f"找到 {len(cases)} 条案例数据")
        
        if len(cases) == 0:
            print("没有找到案例数据，无需迁移")
            conn.close()
            return
        
        # 步骤2: 迁移数据
        print("\n【步骤2】开始迁移数据...")
        migrated_count = 0
        skipped_count = 0
        error_count = 0
        
        for case in cases:
            case_id, title, content, law_type, create_time = case
            
            try:
                # 提取案例信息
                case_type, court_name, judge_date, dispute_point, judgment_result = extract_case_info(content)
                
                # 检查是否已存在（基于标题）
                cursor.execute("SELECT id FROM legal_cases WHERE title = %s", (title,))
                if cursor.fetchone():
                    print(f"  - 跳过已存在的案例: {title}")
                    skipped_count += 1
                    continue
                
                # 插入到 legal_cases 表
                insert_sql = """
                    INSERT INTO legal_cases 
                    (title, case_type, content, court_name, judge_date, 
                     dispute_point, judgment_result, law_type, create_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                cursor.execute(insert_sql, (
                    title,
                    case_type,
                    content[:5000] if content else None,  # 限制长度
                    court_name,
                    judge_date,
                    dispute_point,
                    judgment_result,
                    law_type,
                    create_time
                ))
                
                migrated_count += 1
                
                if migrated_count % 10 == 0:
                    print(f"  已迁移 {migrated_count} 条案例...")
                
            except Exception as e:
                print(f"  ✗ 迁移案例失败 {title}: {e}")
                error_count += 1
                continue
        
        # 提交事务
        conn.commit()
        
        # 步骤3: 删除 legal_articles 表中的案例数据
        print("\n【步骤3】删除 legal_articles 表中的案例数据...")
        cursor.execute("DELETE FROM legal_articles WHERE law_type = '案例'")
        deleted_count = cursor.rowcount
        conn.commit()
        
        print(f"✓ 已删除 {deleted_count} 条案例数据")
        
        # 显示统计
        print("\n" + "=" * 70)
        print("迁移完成！统计信息：")
        print(f"  成功迁移: {migrated_count} 条案例")
        print(f"  跳过记录: {skipped_count} 条（已存在）")
        print(f"  错误数量: {error_count} 条")
        print(f"  从法条表删除: {deleted_count} 条")
        print("=" * 70)
        
        # 验证结果
        cursor.execute("SELECT COUNT(*) FROM legal_cases")
        case_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM legal_articles WHERE law_type = '案例'")
        remaining_count = cursor.fetchone()[0]
        
        print(f"\n当前 legal_cases 表中的案例数: {case_count}")
        print(f"legal_articles 表中剩余的案例数: {remaining_count}")
        
        conn.close()
        
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"\n❌ 迁移过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    migrate_cases()



