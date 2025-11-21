#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复所有法律类型的法条 - 清理并重新导入
支持修复所有类型或指定类型
"""

import pymysql
import os
import sys
from pathlib import Path
import argparse

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from import_laws_data import LawDataImporter, LAW_TYPE_MAPPING

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'hjj060618',
    'database': 'legal_qa',
    'charset': 'utf8mb4'
}

repo_path = r"E:\Laws\Laws"

# 法律类型到文件夹的映射
TYPE_TO_FOLDER = {
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

def fix_law_type(law_type, repo_path_obj):
    """修复指定类型的法律"""
    folder_name = TYPE_TO_FOLDER.get(law_type, law_type)
    folder_path = repo_path_obj / folder_name
    
    if not folder_path.exists():
        print(f"⚠️  跳过：文件夹不存在 - {folder_name}")
        return False
    
    print(f"\n{'=' * 70}")
    print(f"修复 {law_type} 相关法条")
    print(f"{'=' * 70}")
    
    # 步骤1: 清理
    print(f"\n【步骤1】清理现有 {law_type} 数据...")
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM legal_articles WHERE law_type = %s", (law_type,))
    count = cursor.fetchone()[0]
    
    if count > 0:
        print(f"找到 {count:,} 条 {law_type} 相关法条")
        cursor.execute("DELETE FROM legal_articles WHERE law_type = %s", (law_type,))
        deleted = cursor.rowcount
        conn.commit()
        print(f"✓ 已删除 {deleted:,} 条法条")
    else:
        print(f"未找到 {law_type} 相关法条")
    
    conn.close()
    
    # 步骤2: 重新导入
    print(f"\n【步骤2】重新导入 {law_type} 数据...")
    importer = LawDataImporter(db_config, str(repo_path_obj.parent))
    
    try:
        importer.connect_db()
        importer.import_directory(folder_path, law_type)
        importer.close_db()
        
        # 显示结果
        print(f"\n{'=' * 70}")
        print(f"{law_type} 修复完成！")
        print(f"  总文件数: {importer.stats['total_files']}")
        print(f"  成功导入: {importer.stats['imported_articles']} 条法条")
        print(f"  跳过记录: {importer.stats['skipped_articles']} 条")
        print(f"  错误数量: {len(importer.stats['errors'])}")
        print(f"{'=' * 70}")
        
        return True
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    parser = argparse.ArgumentParser(description='修复所有或指定类型的法律法条')
    parser.add_argument('--types', type=str, nargs='+',
                       help='要修复的法律类型（如: 刑法 民法），不指定则修复所有类型')
    parser.add_argument('--repo-path', type=str, default=repo_path,
                       help='LawRefBook/Laws 仓库路径')
    parser.add_argument('--password', type=str, default=db_config['password'],
                       help='数据库密码')
    
    args = parser.parse_args()
    
    db_config['password'] = args.password
    repo_path_obj = Path(args.repo_path)
    
    if not repo_path_obj.exists():
        print(f"❌ 错误：仓库路径不存在: {args.repo_path}")
        return
    
    # 确定要修复的类型
    if args.types:
        law_types = args.types
        print(f"将修复以下类型的法律: {', '.join(law_types)}")
    else:
        law_types = list(TYPE_TO_FOLDER.keys())
        print(f"将修复所有类型的法律: {', '.join(law_types)}")
        confirm = input("\n⚠️  确定要修复所有类型吗？(yes/no): ")
        if confirm.lower() != 'yes':
            print("已取消")
            return
    
    # 修复每个类型
    success_count = 0
    fail_count = 0
    
    for law_type in law_types:
        try:
            if fix_law_type(law_type, repo_path_obj):
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f"❌ 修复 {law_type} 时出错: {e}")
            fail_count += 1
    
    # 最终统计
    print("\n" + "=" * 70)
    print("修复完成！总体统计：")
    print(f"  成功修复: {success_count} 种类型")
    print(f"  失败/跳过: {fail_count} 种类型")
    print("=" * 70)
    
    # 显示数据库总数
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM legal_articles")
    total = cursor.fetchone()[0]
    conn.close()
    
    print(f"\n当前数据库中共有 {total:,} 条法条")

if __name__ == '__main__':
    main()

