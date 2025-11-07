# 前端故障排查指南

## 错误：Cannot find module 'node:url'

### 原因
这个错误通常是因为 Node.js 版本太旧。`node:` 前缀需要 Node.js 14.18.0+ 或 16.0.0+ 才支持。

### 解决方案

#### 方案1：升级 Node.js（推荐）
1. 检查当前 Node.js 版本：
   ```bash
   node -v
   ```

2. 如果版本低于 14.18.0，请升级 Node.js：
   - 访问 https://nodejs.org/ 下载最新 LTS 版本
   - 或者使用 nvm（Node Version Manager）：
     ```bash
     nvm install 16
     nvm use 16
     ```

#### 方案2：降级 Vue CLI（如果无法升级 Node.js）
如果无法升级 Node.js，可以降级 Vue CLI 到兼容版本：

```bash
npm install --save-dev @vue/cli-service@4.5.19
```

#### 方案3：使用兼容配置
在 `vue.config.js` 中添加：

```javascript
module.exports = {
  configureWebpack: {
    resolve: {
      fallback: {
        "url": require.resolve("url/")
      }
    }
  }
}
```

然后安装 url 包：
```bash
npm install --save-dev url
```

## 错误：Unexpected keyword 'case'

### 原因
`case` 是 JavaScript 的关键字，不能用作变量名。

### 解决方案
已修复：将所有 `case` 变量名改为 `caseItem`。

## 其他常见问题

### npm install 失败
1. 清除缓存：
   ```bash
   npm cache clean --force
   ```

2. 删除 node_modules 和 package-lock.json：
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

### 端口被占用
修改 `vue.config.js` 中的端口：
```javascript
devServer: {
  port: 3001  // 改为其他端口
}
```

### 代理不工作
检查后端服务是否正常运行，并确保代理配置正确。

