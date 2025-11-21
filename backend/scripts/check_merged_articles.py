#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查是否有法条合并的问题"""

import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='hjj060618',
    database='legal_qa',
    charset='utf8mb4'
)

cursor = conn.cursor()

print("=" * 70)
print("检查法条合并问题")
print("=" * 70)

# 检查刑法相关法条
print("\n【检查刑法相关法条】")
cursor.execute("""
    SELECT id, title, article_number, LEFT(content, 300) as content_preview
    FROM legal_articles 
    WHERE title LIKE '%刑法%' 
    AND article_number IN ('第一条', '第二条', '第三条', '第四条', '第五条')
    ORDER BY title, article_number
    LIMIT 20
""")

rows = cursor.fetchall()
print(f"\n找到 {len(rows)} 条相关法条：\n")

for row in rows:
    print(f"ID: {row[0]}")
    print(f"标题: {row[1]}")
    print(f"条号: {row[2]}")
    content = row[3] if row[3] else ''
    # 检查内容中是否包含其他条号
    if '第二条' in content or '第三条' in content or '第四条' in content:
        print(f"⚠️  警告：此条内容中包含了其他条号！")
        # 查找内容中的条号
        import re
        other_articles = re.findall(r'第[一二三四五六七八九十百千万\d]+[条章节款项]', content)
        if other_articles:
            print(f"   发现的其他条号: {', '.join(set(other_articles))}")
    print(f"内容预览: {content[:150]}...")
    print("-" * 70)

# 检查是否有内容特别长的法条（可能是合并了多条）
print("\n【检查内容特别长的法条（可能是合并的）】")
cursor.execute("""
    SELECT id, title, article_number, LENGTH(content) as content_length, LEFT(content, 200) as content_preview
    FROM legal_articles 
    WHERE LENGTH(content) > 1000
    ORDER BY LENGTH(content) DESC
    LIMIT 10
""")

long_rows = cursor.fetchall()
print(f"\n找到 {len(long_rows)} 条内容特别长的法条：\n")

for row in long_rows:
    print(f"ID: {row[0]}")
    print(f"标题: {row[1]}")
    print(f"条号: {row[2]}")
    print(f"内容长度: {row[3]} 字符")
    content = row[4] if row[4] else ''
    # 检查内容中是否包含多个条号
    import re
    articles_in_content = re.findall(r'第[一二三四五六七八九十百千万\d]+[条章节款项]', content)
    if len(articles_in_content) > 1:
        print(f"⚠️  警告：此条内容中包含了 {len(articles_in_content)} 个条号！")
        print(f"   发现的条号: {', '.join(set(articles_in_content[:10]))}")
    print(f"内容预览: {content[:150]}...")
    print("-" * 70)

conn.close()
print("\n检查完成！")

