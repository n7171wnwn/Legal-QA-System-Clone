#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""直接验证数据库中的数据 - 显示具体内容"""

import pymysql

print("=" * 70)
print("正在连接数据库并查询数据...")
print("=" * 70)

try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='hjj060618',
        database='legal_qa',
        charset='utf8mb4'
    )
    
    cursor = conn.cursor()
    
    # 1. 查询总数
    print("\n【步骤1】查询总数据量...")
    cursor.execute('SELECT COUNT(*) FROM legal_articles')
    total = cursor.fetchone()[0]
    print(f"✓ 数据库中总共有: {total:,} 条法条")
    
    if total == 0:
        print("\n❌ 数据库中没有数据！")
        conn.close()
        exit(1)
    
    # 2. 查询具体数据
    print("\n【步骤2】查询具体数据（前10条）...")
    cursor.execute('''
        SELECT id, title, article_number, law_type, 
               LEFT(content, 80) as content_preview
        FROM legal_articles 
        ORDER BY id
        LIMIT 10
    ''')
    
    rows = cursor.fetchall()
    print(f"\n✓ 成功查询到 {len(rows)} 条数据：\n")
    
    for i, row in enumerate(rows, 1):
        print(f"【第 {i} 条】")
        print(f"  ID: {row[0]}")
        print(f"  标题: {row[1]}")
        print(f"  条号: {row[2] or '(无)'}")
        print(f"  类型: {row[3] or '未知'}")
        print(f"  内容: {row[4][:80]}..." if row[4] and len(row[4]) > 80 else f"  内容: {row[4] or '(无)'}")
        print()
    
    # 3. 按类型统计
    print("\n【步骤3】按法律类型统计...")
    cursor.execute('''
        SELECT law_type, COUNT(*) as count 
        FROM legal_articles 
        GROUP BY law_type 
        ORDER BY count DESC
        LIMIT 5
    ''')
    
    stats = cursor.fetchall()
    print("\n前5种法律类型：")
    for stat in stats:
        print(f"  {stat[0] or '未知'}: {stat[1]:,} 条")
    
    # 4. 随机查询一条完整数据
    print("\n【步骤4】随机查询一条完整数据...")
    cursor.execute('''
        SELECT id, title, article_number, law_type, content
        FROM legal_articles 
        WHERE article_number IS NOT NULL
        ORDER BY RAND()
        LIMIT 1
    ''')
    
    sample = cursor.fetchone()
    if sample:
        print(f"\n✓ 随机示例数据：")
        print(f"  ID: {sample[0]}")
        print(f"  标题: {sample[1]}")
        print(f"  条号: {sample[2]}")
        print(f"  类型: {sample[3]}")
        print(f"  内容: {sample[4][:200]}..." if sample[4] and len(sample[4]) > 200 else f"  内容: {sample[4]}")
    
    conn.close()
    
    print("\n" + "=" * 70)
    print("✅ 验证完成！数据确实存在于数据库中！")
    print("=" * 70)
    print("\n如果Navicat中看不到数据，请：")
    print("1. 确认连接的是 'legal_qa' 数据库")
    print("2. 确认查看的是 'legal_articles' 表")
    print("3. 右键表 → 刷新（或按F5）")
    print("4. 执行SQL: SELECT COUNT(*) FROM legal_articles;")
    
except pymysql.Error as e:
    print(f"\n❌ 数据库连接错误: {e}")
    print("\n请检查：")
    print("1. MySQL服务是否运行")
    print("2. 数据库 'legal_qa' 是否存在")
    print("3. 用户名和密码是否正确")
except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()

