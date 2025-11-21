#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证导入的数据"""

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
    
    # 统计总数
    cursor.execute('SELECT COUNT(*) FROM legal_articles')
    total = cursor.fetchone()[0]
    print(f'总法条数: {total} 条')
    print('=' * 50)
    
    # 按类型统计
    cursor.execute('''
        SELECT law_type, COUNT(*) as count 
        FROM legal_articles 
        GROUP BY law_type 
        ORDER BY count DESC
    ''')
    results = cursor.fetchall()
    
    print('按法律类型统计:')
    print('-' * 50)
    for row in results:
        law_type = row[0] or '未知'
        count = row[1]
        print(f'{law_type:20s}: {count:6d} 条')
    
    print('=' * 50)
    
    # 显示一些示例数据
    cursor.execute('''
        SELECT title, article_number, law_type 
        FROM legal_articles 
        LIMIT 5
    ''')
    samples = cursor.fetchall()
    
    print('\n示例数据（前5条）:')
    print('-' * 50)
    for sample in samples:
        print(f'标题: {sample[0]}')
        print(f'条号: {sample[1] or "无"}')
        print(f'类型: {sample[2] or "未知"}')
        print()
    
    conn.close()
    print('验证完成！')
    
except Exception as e:
    print(f'错误: {e}')

