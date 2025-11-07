# 前后端连接测试指南

## 问题诊断

### 后端配置
- 端口：8080
- Context Path：`/api`
- 完整API路径：`http://localhost:8080/api/xxx`

### 前端配置
- 端口：3000
- API Base URL：`/api`
- 代理目标：`http://localhost:8080`

## 已修复的问题

### 修复前
```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8080',
    pathRewrite: {
      '^/api': ''  // 这会导致路径不匹配
    }
  }
}
```

### 修复后
```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8080',
    changeOrigin: true,
    ws: true,
    secure: false
    // 去掉了 pathRewrite，因为后端 context-path 已经是 /api
  }
}
```

## 测试步骤

### 1. 确保后端运行
```bash
# 后端应该运行在 http://localhost:8080
# 测试接口：http://localhost:8080/api/legal/article/all
```

### 2. 重启前端开发服务器
```bash
cd frontend
# 停止当前服务器（Ctrl+C）
npm run serve
```

### 3. 测试连接
在浏览器中：
1. 访问 http://localhost:3000
2. 打开浏览器开发者工具（F12）
3. 查看 Network 标签
4. 尝试登录或访问任何需要API的功能
5. 检查请求是否正确转发到后端

### 4. 验证API调用
在浏览器控制台执行：
```javascript
fetch('/api/legal/article/all')
  .then(res => res.json())
  .then(data => console.log('API响应:', data))
  .catch(err => console.error('API错误:', err))
```

## 常见问题

### 问题1：404 Not Found
- **原因**：代理配置错误或后端未运行
- **解决**：检查后端是否在8080端口运行，检查代理配置

### 问题2：CORS错误
- **原因**：后端CORS配置问题
- **解决**：检查 `CorsConfig.java` 配置

### 问题3：网络错误
- **原因**：前端无法连接到后端
- **解决**：检查防火墙，确认端口未被占用

## 正确的请求流程

1. 前端发送请求：`/api/auth/login`
2. 代理拦截：匹配 `/api` 路径
3. 转发到后端：`http://localhost:8080/api/auth/login`
4. 后端处理：Spring Boot 接收请求
5. 返回响应：JSON 数据
6. 代理返回：前端接收到响应

## 验证清单

- [ ] 后端运行在 8080 端口
- [ ] 前端运行在 3000 端口
- [ ] 代理配置正确（无 pathRewrite）
- [ ] CORS 配置正确
- [ ] 浏览器控制台无错误
- [ ] 网络请求显示正确的状态码

