#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试重新导入脚本 - 非交互式版本
只测试导入逻辑，不实际清理数据
"""

import os
import sys
import pymysql
from pathlib import Path

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from import_laws_data import LawDataImporter, DEFAULT_DB_CONFIG

def test_import_single_law():
    """测试导入单个法律（刑法）"""
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'hjj060618',
        'database': 'legal_qa',
        'charset': 'utf8mb4'
    }
    
    repo_path = r"E:\Laws\Laws"
    
    print("=" * 70)
    print("测试重新导入脚本 - 只导入刑法（不清理现有数据）")
    print("=" * 70)
    print(f"仓库路径: {repo_path}")
    print(f"数据库: {db_config['database']}")
    print()
    
    # 检查仓库路径
    if not os.path.exists(repo_path):
        print(f"❌ 错误：仓库路径不存在: {repo_path}")
        return False
    
    # 检查刑法文件夹
    xingfa_path = Path(repo_path) / "刑法"
    if not xingfa_path.exists():
        print(f"❌ 错误：刑法文件夹不存在: {xingfa_path}")
        return False
    
    print(f"✓ 找到刑法文件夹: {xingfa_path}")
    print()
    
    # 创建导入器
    importer = LawDataImporter(db_config, repo_path)
    
    try:
        print("连接数据库...")
        importer.connect_db()
        print("✓ 数据库连接成功")
        print()
        
        # 只导入刑法
        print("开始导入刑法相关法条...")
        print("-" * 70)
        importer.import_directory(xingfa_path, '刑法')
        
        importer.close_db()
        
        # 显示统计
        print("\n" + "=" * 70)
        print("导入完成！统计信息：")
        print(f"  总文件数: {importer.stats['total_files']}")
        print(f"  成功导入: {importer.stats['imported_articles']} 条法条")
        print(f"  跳过记录: {importer.stats['skipped_articles']} 条（已存在）")
        print(f"  错误数量: {len(importer.stats['errors'])}")
        print("=" * 70)
        
        # 验证导入结果
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM legal_articles WHERE law_type = '刑法'")
        count = cursor.fetchone()[0]
        conn.close()
        
        print(f"\n当前数据库中刑法相关法条总数: {count:,} 条")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_import_single_law()

