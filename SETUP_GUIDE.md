# 智慧司法问答系统 - 部署指南

## 重要提示

### 修复 pom.xml 文件

在运行项目之前，请手动修复 `backend/pom.xml` 文件第 18 行：

**将：**

```xml
<n>Legal QA System</n>
```

**改为：**

```xml
<name>Legal QA System</name>
```

## 快速启动步骤

### 1. 环境准备

确保已安装：

- JDK 1.8+
- Maven 3.6+
- Node.js 14+
- MySQL 8.0+

### 2. 数据库配置

```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE legal_qa CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit

# 导入数据库结构
mysql -u root -p legal_qa < backend/src/main/resources/db/migration/schema.sql
```

### 3. 后端配置

编辑 `backend/src/main/resources/application.yml`：

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/legal_qa?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
    username: your_username # 修改为你的数据库用户名
    password: your_password # 修改为你的数据库密码

deepseek:
  api:
    api-key: your-deepseek-api-key-here # 修改为你的DeepSeek API Key
```

### 4. 启动后端

```bash
cd backend
# 先修复pom.xml中的<n>标签
mvn clean install
mvn spring-boot:run
```

后端将在 http://localhost:8080 启动

### 6. 启动前端

```bash
cd frontend
npm install
npm run serve
```

前端将在 http://localhost:3000 启动

## 验证部署

1. 访问前端首页：http://localhost:3000
2. 尝试注册/登录
3. 测试问答功能
4. 访问管理后台（使用 admin 账号）

## 默认账号

- 管理员：`admin` / `123456`
- 普通用户：`user1` / `123456`

## 故障排查

### 后端无法启动

1. 检查数据库连接
2. 检查端口 8080 是否被占用
3. 查看日志文件

### 前端无法连接后端

1. 检查后端是否正常运行
2. 检查 `vue.config.js` 中的代理配置
3. 检查浏览器控制台错误

### DeepSeek API 调用失败

1. 检查 API Key 是否正确
2. 检查 API 额度
3. 查看后端日志

## 生产环境部署

### 后端

```bash
cd backend
mvn clean package
java -jar target/legal-qa-system-1.0.0.jar
```

### 前端

```bash
cd frontend
npm run build
# 将dist目录部署到Web服务器（如Nginx）
```

## 配置 Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 安全建议

1. 修改默认密码
2. 使用 HTTPS
3. 配置防火墙
4. 定期更新依赖
5. 启用日志审计
