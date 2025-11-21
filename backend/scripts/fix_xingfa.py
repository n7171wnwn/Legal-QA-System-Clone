#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复刑法法条 - 清理并重新导入
"""

import pymysql
import os
import sys
from pathlib import Path

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from import_laws_data import LawDataImporter

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'hjj060618',
    'database': 'legal_qa',
    'charset': 'utf8mb4'
}

repo_path = r"E:\Laws\Laws"

print("=" * 70)
print("修复刑法法条 - 清理并重新导入")
print("=" * 70)

# 步骤1: 清理刑法数据
print("\n【步骤1】清理现有刑法数据...")
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

# 查找所有刑法相关的法律标题
cursor.execute("""
    SELECT DISTINCT title 
    FROM legal_articles 
    WHERE law_type = '刑法'
""")
law_titles = [row[0] for row in cursor.fetchall()]

if law_titles:
    print(f"找到 {len(law_titles)} 部刑法相关法律:")
    for title in law_titles[:5]:  # 只显示前5个
        cursor.execute("SELECT COUNT(*) FROM legal_articles WHERE title = %s", (title,))
        count = cursor.fetchone()[0]
        print(f"  - {title}: {count} 条")
    if len(law_titles) > 5:
        print(f"  ... 还有 {len(law_titles) - 5} 部法律")
    
    # 统计总数
    cursor.execute("SELECT COUNT(*) FROM legal_articles WHERE law_type = '刑法'")
    total = cursor.fetchone()[0]
    print(f"\n总计: {total:,} 条刑法相关法条")
    
    # 删除
    print("\n正在删除...")
    cursor.execute("DELETE FROM legal_articles WHERE law_type = '刑法'")
    deleted = cursor.rowcount
    conn.commit()
    print(f"✓ 已删除 {deleted:,} 条法条")
else:
    print("未找到刑法相关法条")

conn.close()

# 步骤2: 重新导入
print("\n【步骤2】重新导入刑法数据...")
importer = LawDataImporter(db_config, repo_path)

try:
    importer.connect_db()
    
    xingfa_path = Path(repo_path) / "刑法"
    if xingfa_path.exists():
        print(f"导入目录: {xingfa_path}")
        importer.import_directory(xingfa_path, '刑法')
    else:
        print(f"❌ 错误：刑法文件夹不存在: {xingfa_path}")
    
    importer.close_db()
    
    # 显示结果
    print("\n" + "=" * 70)
    print("修复完成！统计信息：")
    print(f"  总文件数: {importer.stats['total_files']}")
    print(f"  成功导入: {importer.stats['imported_articles']} 条法条")
    print(f"  跳过记录: {importer.stats['skipped_articles']} 条")
    print(f"  错误数量: {len(importer.stats['errors'])}")
    print("=" * 70)
    
    # 验证
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM legal_articles WHERE law_type = '刑法'")
    count = cursor.fetchone()[0]
    conn.close()
    
    print(f"\n当前数据库中刑法相关法条总数: {count:,} 条")
    
    # 检查第一条是否还有问题
    print("\n【验证】检查第一条是否修复...")
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, article_number, LEFT(content, 300) 
        FROM legal_articles 
        WHERE title='中华人民共和国刑法' AND article_number='第一条'
    """)
    row = cursor.fetchone()
    if row:
        content = row[2] if row[2] else ''
        if '第二条' in content:
            print("⚠️  警告：第一条仍然包含第二条的内容")
            print(f"内容预览: {content[:200]}...")
        else:
            print("✓ 第一条内容正常，不包含第二条")
    conn.close()
    
except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()

