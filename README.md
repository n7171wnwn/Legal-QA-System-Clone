# 智慧司法问答系统

基于 Vue2 + SpringBoot 的智能法律问答系统，使用 DeepSeek API 实现 AI 问答功能。

## 技术栈

### 后端

- Spring Boot 2.7.14
- Spring Data JPA
- MySQL 8.0
- JWT 认证
- DeepSeek API

### 前端

- Vue 2.6.14
- Vue Router
- Vuex
- Element UI
- Axios
- ECharts

## 功能特性

### 用户功能

- ✅ 智能法律问答
- ✅ 问题分类与意图识别
- ✅ 实体识别（法条、罪名、机构等）
- ✅ 答案可信度评估
- ✅ 多轮对话管理
- ✅ 法条查询与解释
- ✅ 法律概念定义
- ✅ 司法程序咨询
- ✅ 案例分析问答
- ✅ 问答历史记录
- ✅ 用户反馈收集

### 管理功能

- ✅ 知识库管理
- ✅ 问答对管理
- ✅ 系统性能监控
- ✅ 用户行为分析
- ✅ 法条管理
- ✅ 案例管理
- ✅ 概念管理

## 项目结构

```
.
├── backend/                 # 后端SpringBoot项目
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/legal/
│   │   │   │   ├── config/      # 配置类
│   │   │   │   ├── controller/  # 控制器
│   │   │   │   ├── dto/         # 数据传输对象
│   │   │   │   ├── entity/      # 实体类
│   │   │   │   ├── repository/  # 数据访问层
│   │   │   │   ├── service/     # 业务逻辑层
│   │   │   │   └── util/        # 工具类
│   │   │   └── resources/
│   │   │       └── application.yml
│   │   └── pom.xml
│   └── README.md
├── frontend/               # 前端Vue2项目
│   ├── src/
│   │   ├── api/           # API接口
│   │   ├── assets/        # 静态资源
│   │   ├── components/    # 组件
│   │   ├── router/        # 路由配置
│   │   ├── store/         # Vuex状态管理
│   │   ├── styles/        # 样式文件
│   │   ├── views/         # 视图组件
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vue.config.js
└── README.md
```

## 快速开始

### 环境要求

- JDK 1.8+
- Maven 3.6+
- Node.js 14+
- MySQL 8.0+

### 后端部署

1. 配置数据库

```sql
CREATE DATABASE legal_qa CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 修改配置
   编辑 `backend/src/main/resources/application.yml`：

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/legal_qa?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
    username: your_username
    password: your_password

deepseek:
  api:
    api-key: your-deepseek-api-key
```

3. 运行后端

```bash
cd backend
mvn clean install
mvn spring-boot:run
```

后端服务将运行在 http://localhost:8080

### 前端部署

1. 安装依赖

```bash
cd frontend
npm install
```

2. 运行开发服务器

```bash
npm run serve
```

前端服务将运行在 http://localhost:3000

3. 构建生产版本

```bash
npm run build
```

## API 接口文档

### 认证接口

- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录

### 问答接口

- `POST /api/qa/ask` - 提问
- `GET /api/qa/history` - 获取问答历史
- `GET /api/qa/conversation/{sessionId}` - 获取会话历史
- `POST /api/qa/feedback` - 提交反馈

### 法律知识接口

- `GET /api/legal/article/search` - 搜索法条
- `GET /api/legal/case/search` - 搜索案例
- `GET /api/legal/concept/search` - 搜索概念

### 管理接口

- `GET /api/admin/knowledge` - 获取知识库列表
- `POST /api/admin/knowledge` - 创建知识
- `PUT /api/admin/knowledge/{id}` - 更新知识
- `DELETE /api/admin/knowledge/{id}` - 删除知识
- `GET /api/admin/stats` - 获取统计数据
- `GET /api/admin/qa` - 获取问答记录

## 数据库设计

### 主要表结构

- `users` - 用户表
- `question_answers` - 问答记录表
- `legal_articles` - 法条表
- `legal_cases` - 案例表
- `legal_concepts` - 概念表
- `knowledge_base` - 知识库表

## 配置说明

### DeepSeek API 配置

1. 注册 DeepSeek 账号并获取 API Key
2. 在 `application.yml` 中配置 `deepseek.api.api-key`
3. 系统将自动使用 DeepSeek API 进行问答生成

### JWT 配置

- Secret Key: 在 `application.yml` 中配置 `jwt.secret`
- Expiration: 默认 24 小时，可在配置文件中修改

## 开发指南

### 添加新的问题类型

1. 在 `DeepSeekService` 中更新问题分类逻辑
2. 在 `QuestionAnswerService` 中添加相应的处理逻辑
3. 在前端界面中添加对应的显示

### 扩展知识库

1. 通过管理后台添加知识
2. 或直接导入数据到数据库
3. 系统会自动索引新知识用于问答

## 注意事项

1. 确保 DeepSeek API Key 有效且有足够的调用额度
2. 数据库连接配置正确
3. 前端代理配置正确（vue.config.js）

## 许可证

MIT License

## 联系方式

如有问题，请联系项目维护者。
