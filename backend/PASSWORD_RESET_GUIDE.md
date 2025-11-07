# 默认账号密码重置指南

## 问题说明

数据库脚本中的BCrypt哈希可能无法正确验证密码 `123456`。

## 解决方案

### 方案1：在前端注册新用户（推荐）

1. 启动前端和后端服务
2. 访问 http://localhost:3000/login
3. 点击"注册"标签
4. 填写信息创建新账号：
   - 用户名：`admin` 或自定义
   - 密码：`123456` 或自定义
   - 其他信息按需填写

### 方案2：通过API注册

使用Postman或curl发送POST请求：

```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "123456",
    "nickname": "管理员",
    "email": "admin@example.com"
  }'
```

### 方案3：在Navicat中手动创建用户

1. 打开Navicat，连接到数据库
2. 执行以下SQL（需要先知道正确的BCrypt哈希）：

```sql
-- 先删除旧用户（如果存在）
DELETE FROM users WHERE username IN ('admin', 'user1');

-- 注意：密码需要是BCrypt加密后的哈希值
-- 由于BCrypt每次生成的哈希都不同，建议使用方案1或方案2
```

### 方案4：使用后端工具生成密码哈希

1. 在 `PasswordHashGenerator.java` 的 `main` 方法中运行
2. 会生成新的BCrypt哈希
3. 使用生成的哈希更新数据库

## 验证密码是否正确

### 方法1：直接登录测试
访问前端登录页面，使用 `admin` / `123456` 尝试登录

### 方法2：检查数据库
在Navicat中查看 `users` 表，确认用户是否存在，密码字段是否为BCrypt哈希格式（以 `$2a$` 开头）

### 方法3：通过API测试
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "123456"
  }'
```

如果返回token，说明密码正确；如果返回"密码错误"，说明需要重置。

## 快速修复步骤

**最简单的方法：**

1. 确保后端运行在 http://localhost:8080
2. 访问前端：http://localhost:3000/login
3. 点击"注册"标签
4. 创建管理员账号：
   - 用户名：`admin`
   - 密码：`123456`
   - 昵称：`管理员`
5. 注册成功后，在数据库中手动将 `user_type` 改为 `1`（管理员）

```sql
UPDATE users SET user_type = 1 WHERE username = 'admin';
```

## 注意事项

- BCrypt哈希每次生成都不同，但都能验证相同的原始密码
- 如果脚本中的哈希无法使用，这是正常的，因为BCrypt的特性
- 建议使用注册功能创建账号，这样密码会被正确加密

