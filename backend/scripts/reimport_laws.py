#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理并重新导入法律法规数据
使用修复后的解析逻辑重新导入数据
"""

import os
import sys
import pymysql
import argparse
from pathlib import Path

# 添加当前目录到路径，以便导入 import_laws_data
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 导入修复后的导入器
try:
    from import_laws_data import LawDataImporter, DEFAULT_DB_CONFIG
except ImportError as e:
    print(f"错误：无法导入 import_laws_data: {e}")
    print("请确保 import_laws_data.py 文件在同一目录下")
    sys.exit(1)

def clear_articles(db_config, clear_all=True, law_titles=None):
    """
    清理法条数据
    
    Args:
        db_config: 数据库配置
        clear_all: 是否清理所有数据
        law_titles: 如果clear_all=False，则只清理指定的法律标题列表
    """
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    
    try:
        if clear_all:
            print("=" * 70)
            print("清理所有法条数据...")
            print("=" * 70)
            
            # 先统计
            cursor.execute("SELECT COUNT(*) FROM legal_articles")
            count = cursor.fetchone()[0]
            print(f"当前数据库中有 {count:,} 条法条")
            
            # 确认
            confirm = input("\n⚠️  确定要删除所有法条数据吗？(yes/no): ")
            if confirm.lower() != 'yes':
                print("已取消操作")
                conn.close()
                return False
            
            # 删除所有数据
            cursor.execute("DELETE FROM legal_articles")
            deleted = cursor.rowcount
            conn.commit()
            print(f"✓ 已删除 {deleted:,} 条法条")
            
        else:
            if not law_titles:
                print("错误：未指定要清理的法律标题")
                conn.close()
                return False
            
            print("=" * 70)
            print(f"清理指定法律的法条数据...")
            print("=" * 70)
            
            # 统计
            placeholders = ','.join(['%s'] * len(law_titles))
            cursor.execute(f"""
                SELECT title, COUNT(*) 
                FROM legal_articles 
                WHERE title IN ({placeholders})
                GROUP BY title
            """, law_titles)
            
            results = cursor.fetchall()
            total = 0
            for title, count in results:
                print(f"  {title}: {count} 条")
                total += count
            
            print(f"\n总计: {total:,} 条法条")
            
            # 确认
            confirm = input("\n⚠️  确定要删除这些法条吗？(yes/no): ")
            if confirm.lower() != 'yes':
                print("已取消操作")
                conn.close()
                return False
            
            # 删除指定法律的数据
            cursor.execute(f"""
                DELETE FROM legal_articles 
                WHERE title IN ({placeholders})
            """, law_titles)
            
            deleted = cursor.rowcount
            conn.commit()
            print(f"✓ 已删除 {deleted:,} 条法条")
        
        conn.close()
        return True
        
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"✗ 清理数据时出错: {e}")
        return False

def reimport_laws(db_config, repo_path, law_types=None):
    """
    重新导入法律法规数据
    
    Args:
        db_config: 数据库配置
        repo_path: LawRefBook/Laws 仓库路径
        law_types: 如果指定，只导入这些类型的法律（如 ['刑法', '民法']）
    """
    print("\n" + "=" * 70)
    print("开始重新导入法律法规数据...")
    print("=" * 70)
    
    importer = LawDataImporter(db_config, repo_path)
    
    try:
        importer.connect_db()
        
        if law_types:
            # 只导入指定类型的法律
            print(f"\n只导入以下类型的法律: {', '.join(law_types)}")
            repo_path_obj = Path(repo_path)
            
            # 法律类型到文件夹的映射
            type_to_folder = {
                '刑法': '刑法',
                '民法': '民法典',
                '行政法': '行政法',
                '经济法': '经济法',
                '社会法': '社会法',
                '程序法': '诉讼与非诉讼程序法',
                '宪法': '宪法',
                '宪法相关法': '宪法相关法',
                '行政法规': '行政法规',
                '部门规章': '部门规章',
                '司法解释': '司法解释',
                '案例': '案例',
                '其他': '其他'
            }
            
            for law_type in law_types:
                folder_name = type_to_folder.get(law_type, law_type)
                folder_path = repo_path_obj / folder_name
                
                if folder_path.exists() and folder_path.is_dir():
                    print(f"\n导入: {folder_name} ({law_type})")
                    importer.import_directory(folder_path, law_type)
                else:
                    print(f"⚠️  文件夹不存在: {folder_name}")
        else:
            # 导入所有数据
            importer.import_all()
        
        importer.close_db()
        
        # 显示最终统计
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM legal_articles")
        total = cursor.fetchone()[0]
        conn.close()
        
        print("\n" + "=" * 70)
        print(f"重新导入完成！当前数据库中共有 {total:,} 条法条")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ 导入过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description='清理并重新导入法律法规数据')
    parser.add_argument('--repo-path', type=str, required=True,
                       help='LawRefBook/Laws 仓库路径')
    parser.add_argument('--host', type=str, default=DEFAULT_DB_CONFIG['host'],
                       help='数据库主机')
    parser.add_argument('--port', type=int, default=DEFAULT_DB_CONFIG['port'],
                       help='数据库端口')
    parser.add_argument('--user', type=str, default=DEFAULT_DB_CONFIG['user'],
                       help='数据库用户名')
    parser.add_argument('--password', type=str, default=DEFAULT_DB_CONFIG['password'],
                       help='数据库密码')
    parser.add_argument('--database', type=str, default=DEFAULT_DB_CONFIG['database'],
                       help='数据库名称')
    parser.add_argument('--clear-all', action='store_true',
                       help='清理所有法条数据')
    parser.add_argument('--clear-types', type=str, nargs='+',
                       help='只清理指定类型的法律（如: --clear-types 刑法 民法）')
    parser.add_argument('--import-types', type=str, nargs='+',
                       help='只导入指定类型的法律（如: --import-types 刑法 民法）')
    parser.add_argument('--skip-clear', action='store_true',
                       help='跳过清理步骤，直接导入（会去重）')
    
    args = parser.parse_args()
    
    db_config = {
        'host': args.host,
        'port': args.port,
        'user': args.user,
        'password': args.password,
        'database': args.database,
        'charset': 'utf8mb4'
    }
    
    # 步骤1: 清理数据
    if not args.skip_clear:
        if args.clear_all:
            success = clear_articles(db_config, clear_all=True)
            if not success:
                print("清理失败，退出")
                return
        elif args.clear_types:
            # 需要先查找这些类型对应的法律标题
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor()
            
            placeholders = ','.join(['%s'] * len(args.clear_types))
            cursor.execute(f"""
                SELECT DISTINCT title 
                FROM legal_articles 
                WHERE law_type IN ({placeholders})
            """, args.clear_types)
            
            law_titles = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            if law_titles:
                success = clear_articles(db_config, clear_all=False, law_titles=law_titles)
                if not success:
                    print("清理失败，退出")
                    return
            else:
                print(f"未找到类型为 {args.clear_types} 的法条")
        else:
            print("⚠️  未指定清理选项，将跳过清理步骤（使用 --skip-clear 明确跳过）")
            confirm = input("是否继续导入？(yes/no): ")
            if confirm.lower() != 'yes':
                return
    
    # 步骤2: 重新导入
    reimport_laws(db_config, args.repo_path, args.import_types)

if __name__ == '__main__':
    main()

