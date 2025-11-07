<template>
  <div class="admin-layout">
    <el-container>
      <el-aside width="200px" class="admin-sidebar">
        <div class="sidebar-header">
          <h2>管理后台</h2>
        </div>
        <el-menu
          :default-active="activeMenu"
          router
          class="sidebar-menu"
        >
          <el-menu-item index="/admin/dashboard">
            <i class="el-icon-data-line"></i>
            <span>数据概览</span>
          </el-menu-item>
          <el-menu-item index="/admin/knowledge">
            <i class="el-icon-document"></i>
            <span>知识库管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/qa">
            <i class="el-icon-chat-line-round"></i>
            <span>问答管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main class="admin-main">
        <div class="admin-header">
          <div class="header-left">
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/admin/dashboard' }">管理后台</el-breadcrumb-item>
              <el-breadcrumb-item>{{ currentTitle }}</el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          <div class="header-right">
            <el-button type="text" @click="goHome">返回首页</el-button>
            <el-button type="text" @click="logout">退出登录</el-button>
          </div>
        </div>
        <router-view></router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'AdminLayout',
  computed: {
    activeMenu() {
      return this.$route.path
    },
    currentTitle() {
      const routeMap = {
        '/admin/dashboard': '数据概览',
        '/admin/knowledge': '知识库管理',
        '/admin/qa': '问答管理'
      }
      return routeMap[this.$route.path] || '管理后台'
    }
  },
  methods: {
    goHome() {
      this.$router.push('/home')
    },
    logout() {
      this.$store.dispatch('user/logout')
      this.$router.push('/home')
      this.$message.success('已退出登录')
    }
  }
}
</script>

<style scoped>
.admin-layout {
  min-height: 100vh;
  background: #f5f5f5;
}

.admin-sidebar {
  background: #001529;
  color: white;
  min-height: 100vh;
}

.sidebar-header {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #1890ff;
}

.sidebar-header h2 {
  color: white;
  margin: 0;
  font-size: 20px;
}

.sidebar-menu {
  border-right: none;
  background: #001529;
}

.sidebar-menu .el-menu-item {
  color: rgba(255, 255, 255, 0.65);
}

.sidebar-menu .el-menu-item:hover,
.sidebar-menu .el-menu-item.is-active {
  background: #1890ff;
  color: white;
}

.admin-main {
  padding: 0;
}

.admin-header {
  background: white;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-right {
  display: flex;
  gap: 10px;
}
</style>

