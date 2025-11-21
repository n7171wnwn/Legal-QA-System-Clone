#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""详细检查数据库中的数据"""

import pymysql

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'hjj060618',
    'database': 'legal_qa',
    'charset': 'utf8mb4'
}

try:
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    
    print("=" * 60)
    print("数据库连接信息:")
    print("=" * 60)
    print(f"主机: {db_config['host']}")
    print(f"数据库: {db_config['database']}")
    print(f"用户: {db_config['user']}")
    print()
    
    # 检查表是否存在
    cursor.execute("SHOW TABLES LIKE 'legal_articles'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        print("❌ 错误: legal_articles 表不存在！")
        print("\n请检查:")
        print("1. 数据库名称是否正确 (应该是: legal_qa)")
        print("2. 表是否已创建")
        conn.close()
        exit(1)
    
    print("✓ legal_articles 表存在")
    print()
    
    # 检查表结构
    print("=" * 60)
    print("表结构:")
    print("=" * 60)
    cursor.execute("DESCRIBE legal_articles")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col[0]:20s} {col[1]:20s} {col[2]:5s} {col[3]:5s}")
    print()
    
    # 统计总数
    cursor.execute('SELECT COUNT(*) FROM legal_articles')
    total = cursor.fetchone()[0]
    print("=" * 60)
    print(f"总法条数: {total:,} 条")
    print("=" * 60)
    print()
    
    # 按类型统计
    cursor.execute('''
        SELECT law_type, COUNT(*) as count 
        FROM legal_articles 
        GROUP BY law_type 
        ORDER BY count DESC
    ''')
    results = cursor.fetchall()
    
    print("按法律类型统计:")
    print("-" * 60)
    for row in results:
        law_type = row[0] or '未知'
        count = row[1]
        percentage = (count / total * 100) if total > 0 else 0
        print(f'{law_type:20s}: {count:6,} 条 ({percentage:5.1f}%)')
    print()
    
    # 显示详细示例数据
    cursor.execute('''
        SELECT id, title, article_number, law_type, 
               LEFT(content, 50) as content_preview,
               create_time
        FROM legal_articles 
        ORDER BY id
        LIMIT 10
    ''')
    samples = cursor.fetchall()
    
    print("=" * 60)
    print("详细示例数据（前10条）:")
    print("=" * 60)
    for i, sample in enumerate(samples, 1):
        print(f"\n[{i}] ID: {sample[0]}")
        print(f"    标题: {sample[1]}")
        print(f"    条号: {sample[2] or '(无)'}")
        print(f"    类型: {sample[3] or '未知'}")
        print(f"    内容预览: {sample[4][:50]}..." if sample[4] and len(sample[4]) > 50 else f"    内容预览: {sample[4] or '(无)'}")
        print(f"    创建时间: {sample[5]}")
    
    print()
    print("=" * 60)
    print("查询完成！")
    print("=" * 60)
    print("\n提示:")
    print("1. 如果使用 Navicat，请确认:")
    print("   - 连接的是 'legal_qa' 数据库")
    print("   - 查看的是 'legal_articles' 表")
    print("   - 刷新表数据（F5）")
    print("\n2. 如果使用 MySQL Workbench，请:")
    print("   - 选择 'legal_qa' 数据库")
    print("   - 执行: SELECT COUNT(*) FROM legal_articles;")
    print("\n3. 通过API查询:")
    print("   - GET http://localhost:8080/api/legal/article/search?keyword=刑法")
    
    conn.close()
    
except pymysql.Error as e:
    print(f"❌ 数据库错误: {e}")
    print("\n请检查:")
    print("1. MySQL服务是否运行")
    print("2. 数据库连接信息是否正确")
    print("3. 数据库 'legal_qa' 是否存在")
except Exception as e:
    print(f"❌ 错误: {e}")

