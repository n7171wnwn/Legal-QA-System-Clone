module.exports = {
  devServer: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        ws: true,
        secure: false,
        logLevel: 'debug'
        // 注意：后端 context-path 是 /api，所以前端请求 /api/xxx 会被代理到 http://localhost:8080/api/xxx
        // 不需要 pathRewrite，因为路径已经匹配
      }
    }
  },
  publicPath: process.env.NODE_ENV === 'production' ? '/legal-qa/' : '/'
}

