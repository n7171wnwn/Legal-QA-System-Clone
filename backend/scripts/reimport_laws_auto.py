#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动重新导入脚本 - 非交互式版本
用于自动化场景，不需要用户确认
"""

import os
import sys
import pymysql
import argparse
from pathlib import Path

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from import_laws_data import LawDataImporter, DEFAULT_DB_CONFIG

def clear_articles_auto(db_config, clear_all=True, law_titles=None, auto_confirm=False):
    """自动清理法条数据（不需要交互确认）"""
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    
    try:
        if clear_all:
            print("=" * 70)
            print("清理所有法条数据...")
            print("=" * 70)
            
            cursor.execute("SELECT COUNT(*) FROM legal_articles")
            count = cursor.fetchone()[0]
            print(f"当前数据库中有 {count:,} 条法条")
            
            if not auto_confirm:
                print("⚠️  警告：将删除所有法条数据！")
                print("   如果确定要继续，请使用 --auto-confirm 参数")
                conn.close()
                return False
            
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
            
            if not auto_confirm:
                print("⚠️  警告：将删除这些法条数据！")
                print("   如果确定要继续，请使用 --auto-confirm 参数")
                conn.close()
                return False
            
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

def main():
    parser = argparse.ArgumentParser(description='自动清理并重新导入法律法规数据（非交互式）')
    parser.add_argument('--repo-path', type=str, required=True,
                       help='LawRefBook/Laws 仓库路径')
    parser.add_argument('--password', type=str, default=DEFAULT_DB_CONFIG['password'],
                       help='数据库密码')
    parser.add_argument('--clear-all', action='store_true',
                       help='清理所有法条数据')
    parser.add_argument('--clear-types', type=str, nargs='+',
                       help='只清理指定类型的法律')
    parser.add_argument('--import-types', type=str, nargs='+',
                       help='只导入指定类型的法律')
    parser.add_argument('--auto-confirm', action='store_true',
                       help='自动确认清理操作（不需要交互）')
    parser.add_argument('--skip-clear', action='store_true',
                       help='跳过清理步骤')
    
    args = parser.parse_args()
    
    db_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': args.password,
        'database': 'legal_qa',
        'charset': 'utf8mb4'
    }
    
    # 清理数据
    if not args.skip_clear:
        if args.clear_all:
            if not clear_articles_auto(db_config, clear_all=True, auto_confirm=args.auto_confirm):
                return
        elif args.clear_types:
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
                if not clear_articles_auto(db_config, clear_all=False, law_titles=law_titles, auto_confirm=args.auto_confirm):
                    return
    
    # 重新导入
    importer = LawDataImporter(db_config, args.repo_path)
    try:
        importer.connect_db()
        
        if args.import_types:
            repo_path_obj = Path(args.repo_path)
            type_to_folder = {
                '刑法': '刑法', '民法': '民法典', '行政法': '行政法',
                '经济法': '经济法', '社会法': '社会法',
                '程序法': '诉讼与非诉讼程序法', '宪法': '宪法',
                '宪法相关法': '宪法相关法', '行政法规': '行政法规',
                '部门规章': '部门规章', '司法解释': '司法解释',
                '案例': '案例', '其他': '其他'
            }
            
            for law_type in args.import_types:
                folder_name = type_to_folder.get(law_type, law_type)
                folder_path = repo_path_obj / folder_name
                if folder_path.exists():
                    importer.import_directory(folder_path, law_type)
        else:
            importer.import_all()
        
        importer.close_db()
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

