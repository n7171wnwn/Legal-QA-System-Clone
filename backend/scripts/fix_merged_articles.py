#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复已合并的法条数据
重新解析法条内容，将合并的法条分割开
"""

import pymysql
import re
from typing import List, Dict

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'hjj060618',
    'database': 'legal_qa',
    'charset': 'utf8mb4'
}

def parse_articles_from_content(content: str, law_title: str) -> List[Dict]:
    """从内容中解析法条"""
    articles = []
    article_markers = []
    
    # 匹配中文数字格式：第一条、第二条等
    for match in re.finditer(r'^第([一二三四五六七八九十百千万\d]+)([条章节款项])', content, re.MULTILINE):
        article_markers.append({
            'pos': match.start(),
            'number': match.group(1),
            'type': match.group(2),
            'full': match.group(0)
        })
    
    # 如果没找到中文数字，尝试阿拉伯数字格式
    if not article_markers:
        for match in re.finditer(r'^第(\d+)([条章节款项])', content, re.MULTILINE):
            article_markers.append({
                'pos': match.start(),
                'number': match.group(1),
                'type': match.group(2),
                'full': match.group(0)
            })
    
    # 根据条号位置分割内容
    if article_markers:
        article_markers.sort(key=lambda x: x['pos'])
        
        for i, marker in enumerate(article_markers):
            article_number = f"第{marker['number']}{marker['type']}"
            
            # 确定本条内容的结束位置（下一条的开始位置，或文件结尾）
            start_pos = marker['pos'] + len(marker['full'])
            end_pos = article_markers[i + 1]['pos'] if i + 1 < len(article_markers) else len(content)
            
            # 提取本条内容
            article_content = content[start_pos:end_pos].strip()
            
            # 清理内容：移除开头的换行和空白
            article_content = re.sub(r'^\s*\n+', '', article_content)
            article_content = re.sub(r'\n+$', '', article_content)
            
            # 如果内容不为空，添加到列表
            if article_content and len(article_content) > 10:
                articles.append({
                    'title': law_title,
                    'article_number': article_number,
                    'content': article_content[:5000]
                })
    
    return articles

def check_if_merged(content: str, current_article_number: str) -> bool:
    """检查内容是否包含其他条号（可能是合并的）"""
    if not content or not current_article_number:
        return False
    
    # 提取当前条号的数字部分
    current_match = re.search(r'第([一二三四五六七八九十百千万\d]+)([条章节款项])', current_article_number)
    if not current_match:
        return False
    
    # 查找内容中所有条号（从行首开始）
    all_articles = re.findall(r'^第([一二三四五六七八九十百千万\d]+)([条章节款项])', content, re.MULTILINE)
    
    # 如果找到多个条号，且包含与当前条号不同的条号，可能是合并的
    if len(all_articles) > 1:
        # 检查是否有其他条号
        for num, typ in all_articles:
            other_article = f"第{num}{typ}"
            if other_article != current_article_number:
                return True
    
    return False

def fix_merged_articles():
    """修复合并的法条"""
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    
    print("=" * 70)
    print("开始修复合并的法条...")
    print("=" * 70)
    
    # 查找可能合并的法条（内容中包含多个条号）
    print("\n【步骤1】查找可能合并的法条...")
    cursor.execute("""
        SELECT id, title, article_number, content
        FROM legal_articles
        WHERE article_number IS NOT NULL
        AND LENGTH(content) > 200
    """)
    
    all_articles = cursor.fetchall()
    print(f"找到 {len(all_articles)} 条法条需要检查")
    
    fixed_count = 0
    skipped_count = 0
    error_count = 0
    
    # 按标题分组处理
    articles_by_title = {}
    for row in all_articles:
        title = row[1]
        if title not in articles_by_title:
            articles_by_title[title] = []
        articles_by_title[title].append({
            'id': row[0],
            'title': row[1],
            'article_number': row[2],
            'content': row[3]
        })
    
    print(f"\n【步骤2】按法律分组，共 {len(articles_by_title)} 部法律")
    
    for title, articles in articles_by_title.items():
        print(f"\n处理: {title} ({len(articles)} 条)")
        
        # 检查是否有合并的问题
        merged_articles = []
        for article in articles:
            if check_if_merged(article['content'], article['article_number']):
                merged_articles.append(article)
        
        if not merged_articles:
            continue
        
        print(f"  发现 {len(merged_articles)} 条可能合并的法条")
        
        # 对于每个合并的法条，尝试重新解析
        for article in merged_articles:
            try:
                # 重新解析内容
                parsed = parse_articles_from_content(article['content'], article['title'])
                
                if len(parsed) > 1:
                    print(f"  ⚠️  ID {article['id']} ({article['article_number']}) 包含 {len(parsed)} 个法条")
                    
                    # 更新当前法条为第一个
                    first_article = parsed[0]
                    if first_article['article_number'] == article['article_number']:
                        # 更新内容
                        cursor.execute("""
                            UPDATE legal_articles 
                            SET content = %s 
                            WHERE id = %s
                        """, (first_article['content'], article['id']))
                        print(f"    ✓ 已更新 ID {article['id']} 的内容")
                        fixed_count += 1
                        
                        # 插入其他法条（如果不存在）
                        for other_article in parsed[1:]:
                            # 检查是否已存在
                            cursor.execute("""
                                SELECT id FROM legal_articles 
                                WHERE title = %s AND article_number = %s
                            """, (other_article['title'], other_article['article_number']))
                            
                            if not cursor.fetchone():
                                cursor.execute("""
                                    INSERT INTO legal_articles 
                                    (title, article_number, content, law_type, is_valid, create_time, update_time)
                                    SELECT %s, %s, %s, law_type, TRUE, NOW(), NOW()
                                    FROM legal_articles WHERE id = %s
                                """, (other_article['title'], other_article['article_number'], 
                                      other_article['content'], article['id']))
                                print(f"    ✓ 已插入新法条: {other_article['article_number']}")
                            else:
                                print(f"    - 跳过已存在的法条: {other_article['article_number']}")
                    else:
                        print(f"    - 条号不匹配，跳过")
                        skipped_count += 1
                else:
                    skipped_count += 1
                    
            except Exception as e:
                print(f"  ✗ 处理 ID {article['id']} 时出错: {e}")
                error_count += 1
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 70)
    print("修复完成！")
    print("=" * 70)
    print(f"修复法条数: {fixed_count}")
    print(f"跳过的法条数: {skipped_count}")
    print(f"错误数: {error_count}")

if __name__ == '__main__':
    fix_merged_articles()

