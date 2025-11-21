#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证修复效果"""

import pymysql
import re

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='hjj060618',
    database='legal_qa',
    charset='utf8mb4'
)

cursor = conn.cursor()

print("=" * 70)
print("验证修复效果 - 检查刑法法条")
print("=" * 70)

# 检查前10条法条
cursor.execute("""
    SELECT id, article_number, LEFT(content, 300) as content_preview
    FROM legal_articles 
    WHERE title='中华人民共和国刑法' 
    AND article_number IN ('第一条', '第二条', '第三条', '第四条', '第五条', 
                           '第六条', '第七条', '第八条', '第九条', '第十条')
    ORDER BY 
        CASE article_number
            WHEN '第一条' THEN 1
            WHEN '第二条' THEN 2
            WHEN '第三条' THEN 3
            WHEN '第四条' THEN 4
            WHEN '第五条' THEN 5
            WHEN '第六条' THEN 6
            WHEN '第七条' THEN 7
            WHEN '第八条' THEN 8
            WHEN '第九条' THEN 9
            WHEN '第十条' THEN 10
        END
    LIMIT 10
""")

rows = cursor.fetchall()

print(f"\n检查前10条法条：\n")

all_ok = True
for row in rows:
    article_num = row[1]
    content = row[2] if row[2] else ''
    
    # 检查内容中是否包含其他条号
    other_articles = re.findall(r'^第[一二三四五六七八九十百千万\d]+[条章节款项]', content, re.MULTILINE)
    
    if len(other_articles) > 1:
        print(f"❌ {article_num}: 包含多个条号标记")
        print(f"   发现的条号: {', '.join(set(other_articles))}")
        print(f"   内容预览: {content[:150]}...")
        all_ok = False
    else:
        print(f"✓ {article_num}: 内容正常")
        print(f"   内容预览: {content[:100]}...")
    
    print()

conn.close()

print("=" * 70)
if all_ok:
    print("✅ 所有检查的法条都正常，修复成功！")
else:
    print("⚠️  发现一些问题，可能需要进一步检查")
print("=" * 70)

