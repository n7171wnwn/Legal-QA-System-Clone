-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    nickname VARCHAR(50),
    avatar VARCHAR(255),
    user_type INT DEFAULT 0 COMMENT '0-普通用户, 1-管理员',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 问答记录表
CREATE TABLE IF NOT EXISTS question_answers (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT,
    question TEXT NOT NULL,
    answer TEXT,
    question_type VARCHAR(50) COMMENT '法条查询、概念定义、程序咨询、案例分析',
    confidence_score DOUBLE COMMENT '可信度评分 0-1',
    entities TEXT COMMENT 'JSON格式存储识别的实体',
    related_laws TEXT COMMENT '相关法条',
    related_cases TEXT COMMENT '相关案例',
    session_id VARCHAR(100) COMMENT '会话ID',
    is_feedback BOOLEAN DEFAULT FALSE,
    feedback_type VARCHAR(20) COMMENT 'positive, negative',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_session_id (session_id),
    INDEX idx_create_time (create_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 法条表
CREATE TABLE IF NOT EXISTS legal_articles (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL COMMENT '法律名称',
    article_number VARCHAR(50) COMMENT '条号',
    content TEXT COMMENT '条文内容',
    law_type VARCHAR(50) COMMENT '民法、刑法、行政法等',
    publish_org VARCHAR(200) COMMENT '发布机构',
    publish_date DATETIME,
    is_valid BOOLEAN DEFAULT TRUE COMMENT '是否有效',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_law_type (law_type),
    INDEX idx_title (title)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 案例表
CREATE TABLE IF NOT EXISTS legal_cases (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL COMMENT '案例标题',
    case_type VARCHAR(100) COMMENT '案由',
    content TEXT COMMENT '案例内容',
    court_name VARCHAR(200) COMMENT '审理法院',
    judge_date DATETIME COMMENT '判决日期',
    dispute_point TEXT COMMENT '核心争议点',
    judgment_result TEXT COMMENT '判决结果',
    law_type VARCHAR(50) COMMENT '法律领域',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_case_type (case_type),
    INDEX idx_law_type (law_type),
    INDEX idx_title (title)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 概念表
CREATE TABLE IF NOT EXISTS legal_concepts (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL COMMENT '概念名称',
    definition TEXT COMMENT '定义',
    explanation TEXT COMMENT '详细解释',
    law_type VARCHAR(50) COMMENT '所属法律领域',
    related_concepts TEXT COMMENT '相关概念',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_law_type (law_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 知识库表
CREATE TABLE IF NOT EXISTS knowledge_base (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    question_type VARCHAR(50),
    tags VARCHAR(500) COMMENT '标签，逗号分隔',
    law_type VARCHAR(50),
    usage_count INT DEFAULT 0 COMMENT '使用次数',
    quality_score DOUBLE COMMENT '质量评分',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_question_type (question_type),
    INDEX idx_law_type (law_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入示例数据
INSERT INTO users (username, password, nickname, user_type) VALUES
('admin', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iwK8pQMW', '管理员', 1),
('user1', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iwK8pQMW', '测试用户', 0);

-- 密码为: 123456

