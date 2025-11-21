#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查具体的法条内容"""

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

# 检查刑法的第一条
cursor.execute("""
    SELECT id, article_number, content 
    FROM legal_articles 
    WHERE title='中华人民共和国刑法' AND article_number='第一条'
""")

row = cursor.fetchone()
if row:
    print(f"ID: {row[0]}")
    print(f"条号: {row[1]}")
    print(f"\n内容（前500字符）:")
    print(row[2][:500] if row[2] else '无内容')
    
    # 检查内容中是否包含其他条号
    if row[2]:
        other_articles = re.findall(r'^第[一二三四五六七八九十百千万\d]+[条章节款项]', row[2], re.MULTILINE)
        if len(other_articles) > 1:
            print(f"\n⚠️ 发现 {len(other_articles)} 个条号标记:")
            for art in other_articles:
                print(f"  - {art}")

conn.close()

