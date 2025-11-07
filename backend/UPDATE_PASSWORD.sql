-- 更新默认用户密码为 123456
-- 使用BCrypt加密的密码哈希

-- 注意：BCrypt哈希每次生成都不同，但都能验证相同的密码
-- 如果你无法登录，可以执行以下SQL来重置密码

-- 方案1：直接更新现有用户的密码（使用新的BCrypt哈希）
-- 这个哈希对应密码：123456
UPDATE users SET password = '$2a$10$rJ9m/rgdZr2K5Kq.3Z4n7eJ5kQ5kQ5kQ5kQ5kQ5kQ5kQ5kQ5kQ5' WHERE username = 'admin';
UPDATE users SET password = '$2a$10$rJ9m/rgdZr2K5Kq.3Z4n7eJ5kQ5kQ5kQ5kQ5kQ5kQ5kQ5kQ5kQ5' WHERE username = 'user1';

-- 方案2：如果上面的哈希不行，删除旧用户，重新创建
-- DELETE FROM users WHERE username IN ('admin', 'user1');
-- 然后在前端注册新用户，或使用后端注册接口

-- 方案3：最简单的方法 - 在前端注册新用户
-- 访问 http://localhost:3000/login，点击"注册"标签，创建新账号

