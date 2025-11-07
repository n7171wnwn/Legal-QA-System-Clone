# 智慧司法问答系统 - 前端

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 配置代理

确保 `vue.config.js` 中的代理配置正确指向后端服务。

### 3. 运行开发服务器

```bash
npm run serve
```

前端服务将运行在 http://localhost:3000

### 4. 构建生产版本

```bash
npm run build
```

## 项目结构

```
src/
├── api/           # API接口封装
├── assets/        # 静态资源
├── components/    # 公共组件
├── router/        # 路由配置
├── store/         # Vuex状态管理
├── styles/        # 样式文件
└── views/         # 页面组件
    ├── Home.vue           # 首页
    ├── Chat.vue           # 问答页面
    ├── Knowledge.vue      # 知识库
    ├── Profile.vue        # 个人中心
    ├── Login.vue          # 登录页
    └── admin/             # 管理后台
        ├── Layout.vue     # 管理后台布局
        ├── Dashboard.vue  # 数据概览
        ├── Knowledge.vue  # 知识库管理
        └── QA.vue         # 问答管理
```

## 技术栈

- Vue 2.6.14
- Vue Router 3.5.4
- Vuex 3.6.2
- Element UI 2.15.13
- Axios 1.4.0
- ECharts 5.4.2

