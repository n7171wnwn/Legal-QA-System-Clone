-- 法律法规数据查询SQL
-- 在Navicat中执行这些查询来查看导入的数据

-- 1. 查看总数据量
SELECT COUNT(*) AS '总法条数' FROM legal_articles;

-- 2. 按法律类型统计
SELECT 
    COALESCE(law_type, '未知') AS '法律类型',
    COUNT(*) AS '数量',
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM legal_articles), 2) AS '占比(%)'
FROM legal_articles
GROUP BY law_type
ORDER BY COUNT(*) DESC;

-- 3. 查看前20条数据（详细）
SELECT 
    id AS 'ID',
    title AS '标题',
    article_number AS '条号',
    law_type AS '法律类型',
    LEFT(content, 100) AS '内容预览',
    publish_org AS '发布机构',
    publish_date AS '发布日期',
    is_valid AS '是否有效',
    create_time AS '创建时间'
FROM legal_articles
ORDER BY id
LIMIT 20;

-- 4. 查看刑法相关法条
SELECT 
    id,
    title,
    article_number,
    LEFT(content, 200) AS content_preview
FROM legal_articles
WHERE law_type = '刑法'
ORDER BY id
LIMIT 10;

-- 5. 查看民法相关法条
SELECT 
    id,
    title,
    article_number,
    LEFT(content, 200) AS content_preview
FROM legal_articles
WHERE law_type = '民法'
ORDER BY id
LIMIT 10;

-- 6. 搜索包含特定关键词的法条
-- 例如：搜索包含"刑法"的法条
SELECT 
    id,
    title,
    article_number,
    law_type,
    LEFT(content, 150) AS content_preview
FROM legal_articles
WHERE title LIKE '%刑法%' OR content LIKE '%刑法%'
LIMIT 20;

-- 7. 查看最近导入的数据
SELECT 
    id,
    title,
    article_number,
    law_type,
    create_time
FROM legal_articles
ORDER BY create_time DESC
LIMIT 20;

-- 8. 查看各法律类型的详细统计
SELECT 
    law_type AS '法律类型',
    COUNT(*) AS '总数',
    COUNT(DISTINCT title) AS '法律数量',
    MIN(create_time) AS '最早导入时间',
    MAX(create_time) AS '最新导入时间'
FROM legal_articles
GROUP BY law_type
ORDER BY COUNT(*) DESC;

