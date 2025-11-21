#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 LawRefBook/Laws 仓库导入法律法规数据到 MySQL 数据库
"""

import os
import re
import sys
import json
import pymysql
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import argparse

# 数据库配置（从 application.yml 读取或使用命令行参数）
DEFAULT_DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'hjj060618',
    'database': 'legal_qa',
    'charset': 'utf8mb4'
}

# 法律类型映射（从文件夹名称映射到数据库中的law_type）
LAW_TYPE_MAPPING = {
    '刑法': '刑法',
    '民法典': '民法',
    '民法商法': '民法',
    '宪法': '宪法',
    '宪法相关法': '宪法相关法',
    '行政法': '行政法',
    '行政法规': '行政法规',
    '经济法': '经济法',
    '社会法': '社会法',
    '诉讼与非诉讼程序法': '程序法',
    '部门规章': '部门规章',
    '司法解释': '司法解释',
    '案例': '案例',
    '其他': '其他'
}


class LawDataImporter:
    def __init__(self, db_config: Dict, laws_repo_path: str):
        """
        初始化导入器
        
        Args:
            db_config: 数据库配置
            laws_repo_path: LawRefBook/Laws 仓库路径
        """
        self.db_config = db_config
        self.laws_repo_path = Path(laws_repo_path)
        self.connection = None
        self.stats = {
            'total_files': 0,
            'imported_articles': 0,
            'skipped_articles': 0,
            'errors': []
        }

    def connect_db(self):
        """连接数据库"""
        try:
            self.connection = pymysql.connect(**self.db_config)
            print(f"✓ 成功连接到数据库: {self.db_config['database']}")
        except Exception as e:
            print(f"✗ 数据库连接失败: {e}")
            sys.exit(1)

    def close_db(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            print("✓ 数据库连接已关闭")

    def parse_markdown_file(self, file_path: Path) -> List[Dict]:
        """
        解析markdown文件，提取法条信息
        
        Args:
            file_path: markdown文件路径
            
        Returns:
            法条列表，每个法条包含 title, article_number, content 等信息
        """
        articles = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.stats['errors'].append(f"读取文件失败 {file_path}: {e}")
            return articles

        # 获取文件名作为法律名称
        law_title = file_path.stem
        
        # 尝试从文件内容中提取法律名称（通常在文件开头）
        title_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
        if title_match:
            law_title = title_match.group(1).strip()
        
        # 提取发布机构和日期（如果存在）
        publish_org = None
        publish_date = None
        
        # 尝试提取发布信息
        # 匹配多种格式：发布机关、发布机构、制定机关等
        org_patterns = [
            r'发布[机关|机构][：:]\s*(.+?)(?:\n|$)',
            r'制定[机关|机构][：:]\s*(.+?)(?:\n|$)',
            r'颁布[机关|机构][：:]\s*(.+?)(?:\n|$)',
        ]
        for pattern in org_patterns:
            org_match = re.search(pattern, content)
            if org_match:
                publish_org = org_match.group(1).strip()
                break
        
        # 尝试提取发布日期
        date_patterns = [
            r'发布[日期|时间][：:]\s*(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?)',
            r'颁布[日期|时间][：:]\s*(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?)',
            r'施行[日期|时间][：:]\s*(\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?)',
            r'(\d{4})年(\d{1,2})月(\d{1,2})日',  # 直接匹配日期格式
        ]
        for pattern in date_patterns:
            date_match = re.search(pattern, content)
            if date_match:
                if len(date_match.groups()) == 3:
                    # 匹配到年月日格式
                    year, month, day = date_match.groups()
                    date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                else:
                    date_str = date_match.group(1).replace('年', '-').replace('月', '-').replace('日', '')
                
                # 标准化日期格式
                date_str = re.sub(r'[年月日]', '-', date_str).strip('-')
                parts = date_str.split('-')
                if len(parts) >= 3:
                    date_str = f"{parts[0]}-{parts[1].zfill(2)}-{parts[2].zfill(2)}"
                elif len(parts) == 2:
                    date_str = f"{parts[0]}-{parts[1].zfill(2)}-01"
                
                try:
                    publish_date = datetime.strptime(date_str, '%Y-%m-%d')
                except:
                    try:
                        publish_date = datetime.strptime(date_str, '%Y-%m')
                    except:
                        pass
                if publish_date:
                    break

        # 解析法条内容
        # 改进的解析方法：先找到所有条号位置，然后分割内容
        # 匹配所有条号位置（包括中文数字和阿拉伯数字）
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
            # 按位置排序
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
                if article_content and len(article_content) > 10:  # 至少10个字符
                    articles.append({
                        'title': law_title,
                        'article_number': article_number,
                        'content': article_content[:5000],  # 限制长度
                        'publish_org': publish_org,
                        'publish_date': publish_date
                    })
        
        # 如果仍然没有找到，将整个文件内容作为一条记录
        if not articles and content.strip():
            # 清理内容，移除markdown格式
            clean_content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)
            clean_content = clean_content.strip()
            
            if len(clean_content) > 50:  # 只处理有实际内容的文件
                articles.append({
                    'title': law_title,
                    'article_number': None,
                    'content': clean_content[:5000],
                    'publish_org': publish_org,
                    'publish_date': publish_date
                })

        return articles

    def get_law_type_from_path(self, file_path: Path) -> Optional[str]:
        """
        从文件路径推断法律类型
        
        Args:
            file_path: 文件路径
            
        Returns:
            法律类型
        """
        # 获取文件相对于仓库根目录的路径
        try:
            relative_path = file_path.relative_to(self.laws_repo_path)
            # 获取第一级目录名
            first_dir = relative_path.parts[0] if relative_path.parts else None
            
            if first_dir and first_dir in LAW_TYPE_MAPPING:
                return LAW_TYPE_MAPPING[first_dir]
        except:
            pass
        
        return None

    def import_article(self, article: Dict, law_type: Optional[str]) -> bool:
        """
        导入单条法条到数据库
        
        Args:
            article: 法条数据
            law_type: 法律类型
            
        Returns:
            是否成功
        """
        try:
            cursor = self.connection.cursor()
            
            # 检查是否已存在（根据title和article_number）
            check_sql = """
                SELECT id FROM legal_articles 
                WHERE title = %s AND (article_number = %s OR (%s IS NULL AND article_number IS NULL))
            """
            cursor.execute(check_sql, (article['title'], article['article_number'], article['article_number']))
            existing = cursor.fetchone()
            
            if existing:
                self.stats['skipped_articles'] += 1
                return False
            
            # 插入新记录
            insert_sql = """
                INSERT INTO legal_articles 
                (title, article_number, content, law_type, publish_org, publish_date, is_valid, create_time, update_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """
            
            cursor.execute(insert_sql, (
                article['title'],
                article['article_number'],
                article['content'],
                law_type,
                article['publish_org'],
                article['publish_date'],
                True
            ))
            
            self.connection.commit()
            self.stats['imported_articles'] += 1
            return True
            
        except Exception as e:
            self.connection.rollback()
            error_msg = f"导入法条失败 {article.get('title', 'Unknown')}: {e}"
            self.stats['errors'].append(error_msg)
            print(f"  ✗ {error_msg}")
            return False

    def import_directory(self, directory: Path, law_type: Optional[str] = None):
        """
        导入目录下的所有markdown文件
        
        Args:
            directory: 目录路径
            law_type: 法律类型（如果为None，则从路径推断）
        """
        if not directory.exists():
            print(f"✗ 目录不存在: {directory}")
            return
        
        # 如果未指定law_type，从路径推断
        if law_type is None:
            law_type = self.get_law_type_from_path(directory)
        
        print(f"\n处理目录: {directory.name} (类型: {law_type or '未知'})")
        
        # 查找所有markdown文件
        md_files = list(directory.rglob('*.md'))
        self.stats['total_files'] += len(md_files)
        
        for md_file in md_files:
            print(f"  处理文件: {md_file.name}")
            articles = self.parse_markdown_file(md_file)
            
            for article in articles:
                self.import_article(article, law_type)
            
            if articles:
                print(f"    ✓ 提取了 {len(articles)} 条法条")

    def import_all(self):
        """导入整个仓库的数据"""
        if not self.laws_repo_path.exists():
            print(f"✗ 仓库路径不存在: {self.laws_repo_path}")
            return
        
        print(f"开始导入数据从: {self.laws_repo_path}")
        
        # 遍历各个法律分类目录
        for category_dir in self.laws_repo_path.iterdir():
            if category_dir.is_dir() and not category_dir.name.startswith('.'):
                # 跳过一些不需要的目录
                if category_dir.name in ['.git', 'scripts', '.github', 'DLC']:
                    continue
                
                self.import_directory(category_dir)
        
        # 打印统计信息
        print("\n" + "="*50)
        print("导入完成！统计信息：")
        print(f"  总文件数: {self.stats['total_files']}")
        print(f"  成功导入: {self.stats['imported_articles']} 条法条")
        print(f"  跳过记录: {self.stats['skipped_articles']} 条（已存在）")
        print(f"  错误数量: {len(self.stats['errors'])}")
        
        if self.stats['errors']:
            print("\n错误列表：")
            for error in self.stats['errors'][:10]:  # 只显示前10个错误
                print(f"  - {error}")


def main():
    parser = argparse.ArgumentParser(description='从 LawRefBook/Laws 仓库导入数据到 MySQL 数据库')
    parser.add_argument('--repo-path', type=str, required=True,
                       help='LawRefBook/Laws 仓库路径')
    parser.add_argument('--host', type=str, default=DEFAULT_DB_CONFIG['host'],
                       help='数据库主机')
    parser.add_argument('--port', type=int, default=DEFAULT_DB_CONFIG['port'],
                       help='数据库端口')
    parser.add_argument('--user', type=str, default=DEFAULT_DB_CONFIG['user'],
                       help='数据库用户名')
    parser.add_argument('--password', type=str, default=DEFAULT_DB_CONFIG['password'],
                       help='数据库密码')
    parser.add_argument('--database', type=str, default=DEFAULT_DB_CONFIG['database'],
                       help='数据库名称')
    
    args = parser.parse_args()
    
    db_config = {
        'host': args.host,
        'port': args.port,
        'user': args.user,
        'password': args.password,
        'database': args.database,
        'charset': 'utf8mb4'
    }
    
    importer = LawDataImporter(db_config, args.repo_path)
    
    try:
        importer.connect_db()
        importer.import_all()
    finally:
        importer.close_db()


if __name__ == '__main__':
    main()

