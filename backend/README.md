# 智慧司法问答系统 - 后端

## 快速开始

### 1. 配置数据库

创建MySQL数据库：
```sql
CREATE DATABASE legal_qa CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

执行初始化脚本：
```bash
mysql -u root -p legal_qa < src/main/resources/db/migration/schema.sql
```

### 2. 配置DeepSeek API

在 `application.yml` 中设置你的DeepSeek API Key：
```yaml
deepseek:
  api:
    api-key: your-deepseek-api-key-here
```

### 3. 运行项目

```bash
mvn clean install
mvn spring-boot:run
```

后端服务将运行在 http://localhost:8080

## API文档

### 认证
- `POST /api/auth/register` - 注册
- `POST /api/auth/login` - 登录

### 问答
- `POST /api/qa/ask` - 提问
- `GET /api/qa/history` - 问答历史
- `GET /api/qa/conversation/{sessionId}` - 会话历史
- `POST /api/qa/feedback` - 反馈

### 法律知识
- `GET /api/legal/article/search` - 搜索法条
- `GET /api/legal/case/search` - 搜索案例
- `GET /api/legal/concept/search` - 搜索概念

## 默认账号

- 管理员：admin / 123456
- 普通用户：user1 / 123456

