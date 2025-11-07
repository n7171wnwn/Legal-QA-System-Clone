# Navicat 连接数据库指南

## 连接信息

根据 `backend/src/main/resources/application.yml` 配置：

- **数据库类型**：MySQL
- **主机名/IP地址**：`localhost` 或 `127.0.0.1`
- **端口**：`3306`（MySQL默认端口）
- **用户名**：`root`
- **密码**：`hjj060618`（请根据你的实际密码修改）
- **数据库名**：`legal_qa`

## Navicat 连接步骤

### 1. 打开 Navicat
启动 Navicat for MySQL（或 Navicat Premium）

### 2. 创建新连接

**方法一：通过连接向导**
1. 点击左上角 **"连接"** 按钮
2. 选择 **"MySQL"**
3. 弹出连接配置窗口

**方法二：直接创建**
1. 右键点击左侧连接列表
2. 选择 **"新建连接"** → **"MySQL"**

### 3. 填写连接信息

在连接配置窗口中填写：

```
连接名：legal_qa（可以自定义，如：智慧司法系统）
主机名或IP地址：localhost
端口：3306
用户名：root
密码：hjj060618（根据你的实际密码修改）
```

### 4. 高级设置（可选但推荐）

点击 **"高级"** 选项卡，设置：

```
字符集：utf8mb4
排序规则：utf8mb4_unicode_ci
```

### 5. 测试连接

1. 点击 **"测试连接"** 按钮
2. 如果显示 **"连接成功"**，说明配置正确
3. 点击 **"确定"** 保存连接

### 6. 打开数据库

1. 双击连接名称，输入密码（如果设置了保存密码则自动连接）
2. 展开连接，找到 `legal_qa` 数据库
3. 双击 `legal_qa` 数据库，即可查看所有表

## 数据库表结构

连接成功后，你应该能看到以下表：

- `users` - 用户表
- `question_answers` - 问答记录表
- `legal_articles` - 法条表
- `legal_cases` - 案例表
- `legal_concepts` - 概念表
- `knowledge_base` - 知识库表

## 常见问题

### 问题1：连接失败 - 无法连接到MySQL服务器

**可能原因：**
- MySQL服务未启动
- 端口被占用
- 防火墙阻止连接

**解决方法：**
1. 检查MySQL服务是否启动：
   ```powershell
   # Windows
   net start MySQL
   # 或
   services.msc  # 查找MySQL服务并启动
   ```

2. 检查端口是否被占用：
   ```powershell
   netstat -ano | findstr :3306
   ```

3. 检查防火墙设置

### 问题2：连接失败 - Access denied

**可能原因：**
- 用户名或密码错误
- 用户没有远程连接权限

**解决方法：**
1. 确认用户名和密码正确
2. 如果是远程连接，需要授权：
   ```sql
   GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'your_password' WITH GRANT OPTION;
   FLUSH PRIVILEGES;
   ```

### 问题3：找不到数据库

**可能原因：**
- 数据库未创建
- 数据库名称拼写错误

**解决方法：**
1. 检查数据库是否存在：
   ```sql
   SHOW DATABASES;
   ```

2. 如果不存在，创建数据库：
   ```sql
   CREATE DATABASE legal_qa CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. 执行初始化脚本：
   ```bash
   mysql -u root -p legal_qa < backend/src/main/resources/db/migration/schema.sql
   ```

## 验证连接

连接成功后，可以执行以下SQL验证：

```sql
-- 查看所有表
SHOW TABLES;

-- 查看用户表数据
SELECT * FROM users;

-- 查看表结构
DESCRIBE users;
```

## 安全建议

1. **不要使用 root 用户**：建议创建专用数据库用户
2. **设置强密码**：使用复杂密码
3. **限制访问IP**：只允许特定IP连接
4. **定期备份**：使用Navicat的备份功能

## 创建专用用户（可选）

如果你想创建专用数据库用户而不是使用root：

```sql
-- 创建用户
CREATE USER 'legal_user'@'localhost' IDENTIFIED BY 'your_password';

-- 授权
GRANT ALL PRIVILEGES ON legal_qa.* TO 'legal_user'@'localhost';

-- 刷新权限
FLUSH PRIVILEGES;
```

然后在Navicat中使用这个新用户连接。

