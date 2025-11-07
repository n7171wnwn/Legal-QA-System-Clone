# 快速修复默认账号密码问题

## 问题
数据库脚本中的BCrypt哈希可能无法验证密码 `123456`。

## 最快解决方法

### 步骤1：确保后端运行
后端应该已经在 http://localhost:8080 运行

### 步骤2：通过前端注册新账号

1. 访问前端登录页面：http://localhost:3000/login
2. 点击 **"注册"** 标签
3. 填写信息：
   ```
   用户名：admin
   密码：123456
   昵称：管理员
   邮箱：admin@example.com（可选）
   手机号：（可选）
   ```
4. 点击注册

### 步骤3：设置为管理员（如果需要）

注册后，在Navicat中执行：

```sql
UPDATE users SET user_type = 1 WHERE username = 'admin';
```

## 或者通过API注册

使用浏览器控制台或Postman：

```javascript
fetch('http://localhost:8080/api/auth/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    username: 'admin',
    password: '123456',
    nickname: '管理员',
    email: 'admin@example.com'
  })
})
.then(res => res.json())
.then(data => {
  console.log('注册成功:', data);
})
.catch(err => console.error('注册失败:', err));
```

## 验证

注册成功后，使用 `admin` / `123456` 登录即可。

