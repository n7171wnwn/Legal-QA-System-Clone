#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证案例迁移结果"""

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
print("验证案例迁移结果")
print("=" * 70)

# 检查 legal_cases 表
print("\n【legal_cases 表】")
cursor.execute("SELECT COUNT(*) FROM legal_cases")
case_count = cursor.fetchone()[0]
print(f"案例总数: {case_count}")

# 检查 legal_articles 表中是否还有案例
print("\n【legal_articles 表】")
cursor.execute("SELECT COUNT(*) FROM legal_articles WHERE law_type = '案例'")
remaining_count = cursor.fetchone()[0]
print(f"剩余的案例数: {remaining_count}")

# 显示一些案例示例
print("\n【案例示例（前5条）】")
cursor.execute("""
    SELECT id, title, case_type, court_name, law_type
    FROM legal_cases
    ORDER BY id
    LIMIT 5
""")

rows = cursor.fetchall()
for i, row in enumerate(rows, 1):
    print(f"\n[{i}] ID: {row[0]}")
    print(f"    标题: {row[1]}")
    print(f"    案由: {row[2] or '(无)'}")
    print(f"    法院: {row[3] or '(无)'}")
    print(f"    类型: {row[4] or '(无)'}")

# 统计按类型分布
print("\n【按法律类型统计】")
cursor.execute("""
    SELECT law_type, COUNT(*) as count
    FROM legal_cases
    GROUP BY law_type
    ORDER BY count DESC
""")

stats = cursor.fetchall()
for stat in stats:
    print(f"  {stat[0] or '未知'}: {stat[1]} 条")

conn.close()

print("\n" + "=" * 70)
if remaining_count == 0:
    print("✅ 迁移成功！所有案例已从 legal_articles 表迁移到 legal_cases 表")
else:
    print(f"⚠️  还有 {remaining_count} 条案例在 legal_articles 表中")
print("=" * 70)



