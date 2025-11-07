# 智慧司法问答系统 - 项目总结

## 项目概述

已完成一个基于Vue2 + SpringBoot的智慧司法问答系统，集成DeepSeek API实现AI问答功能。

## 已完成功能

### 后端 (SpringBoot)

✅ **核心功能模块**
- 用户认证与授权（JWT）
- 智能问答服务（集成DeepSeek API）
- 问题分类与意图识别
- 实体识别（法条、罪名、机构、概念）
- 答案可信度评估
- 知识检索模块
- 多轮对话管理

✅ **数据管理**
- 用户管理
- 问答记录管理
- 法条管理
- 案例管理
- 概念管理
- 知识库管理

✅ **API接口**
- 认证接口（登录、注册）
- 问答接口（提问、历史、反馈）
- 法律知识接口（法条、案例、概念查询）
- 管理接口（知识库管理、统计、问答管理）

### 前端 (Vue2)

✅ **用户界面**
- 首页（问题输入、快捷功能、热门问题）
- 智能问答页面（对话界面、实体识别、法条案例展示）
- 法律知识库（法条、案例、概念浏览）
- 个人中心（问答历史、收藏、个人信息）

✅ **管理后台**
- 数据概览（统计图表、热门问题）
- 知识库管理（增删改查）
- 问答管理（查看、分析）

✅ **UI/UX**
- 响应式设计
- Element UI组件库
- 可视化数据展示（ECharts）
- 友好的交互体验

## 技术架构

### 后端技术栈
- Spring Boot 2.7.14
- Spring Data JPA
- MySQL 8.0
- Redis
- JWT认证
- DeepSeek API集成
- OkHttp客户端

### 前端技术栈
- Vue 2.6.14
- Vue Router 3.5.4
- Vuex 3.6.2
- Element UI 2.15.13
- Axios 1.4.0
- ECharts 5.4.2

## 项目结构

```
.
├── backend/                    # 后端SpringBoot项目
│   ├── src/main/java/com/legal/
│   │   ├── config/            # 配置类
│   │   ├── controller/        # 控制器
│   │   ├── dto/              # 数据传输对象
│   │   ├── entity/           # 实体类
│   │   ├── repository/       # 数据访问层
│   │   ├── service/          # 业务逻辑层
│   │   └── util/             # 工具类
│   ├── src/main/resources/
│   │   ├── application.yml   # 配置文件
│   │   └── db/migration/     # 数据库脚本
│   └── pom.xml
│
├── frontend/                   # 前端Vue2项目
│   ├── src/
│   │   ├── api/              # API接口
│   │   ├── components/       # 组件
│   │   ├── router/           # 路由
│   │   ├── store/            # 状态管理
│   │   ├── views/            # 视图
│   │   └── styles/           # 样式
│   ├── package.json
│   └── vue.config.js
│
└── README.md                   # 项目说明
```

## 部署说明

### 后端部署

1. **配置数据库**
   ```sql
   CREATE DATABASE legal_qa CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   mysql -u root -p legal_qa < backend/src/main/resources/db/migration/schema.sql
   ```

2. **配置Redis**
   - 启动Redis服务

3. **配置DeepSeek API**
   - 在 `application.yml` 中设置API Key

4. **运行后端**
   ```bash
   cd backend
   mvn clean install
   mvn spring-boot:run
   ```

### 前端部署

1. **安装依赖**
   ```bash
   cd frontend
   npm install
   ```

2. **运行开发服务器**
   ```bash
   npm run serve
   ```

3. **构建生产版本**
   ```bash
   npm run build
   ```

## 默认账号

- 管理员：admin / 123456
- 普通用户：user1 / 123456

## 注意事项

1. **DeepSeek API配置**
   - 需要在 `application.yml` 中配置有效的API Key
   - 确保API Key有足够的调用额度

2. **数据库配置**
   - 修改 `application.yml` 中的数据库连接信息
   - 执行数据库初始化脚本

3. **前端代理配置**
   - 确保 `vue.config.js` 中的代理配置正确

4. **pom.xml修复**
   - 需要手动将 `<n>` 标签改为 `<name>` 标签（第18行）

## 后续优化建议

1. **功能增强**
   - 添加文件上传功能（合同、证据图片分析）
   - 实现语音输入功能
   - 添加更多可视化图表
   - 实现报告导出功能

2. **性能优化**
   - 添加Redis缓存
   - 优化数据库查询
   - 实现分页加载
   - 添加CDN加速

3. **安全增强**
   - 添加请求限流
   - 实现更严格的权限控制
   - 添加数据加密
   - 实现日志审计

4. **用户体验**
   - 添加加载动画
   - 优化移动端适配
   - 添加多语言支持
   - 实现暗色模式

## 问题排查

### 常见问题

1. **后端启动失败**
   - 检查数据库连接配置
   - 确认Redis服务运行
   - 检查端口占用

2. **前端无法连接后端**
   - 检查代理配置
   - 确认后端服务运行
   - 检查CORS配置

3. **DeepSeek API调用失败**
   - 检查API Key是否正确
   - 确认API额度充足
   - 检查网络连接

## 联系支持

如有问题，请查看项目文档或联系开发团队。

