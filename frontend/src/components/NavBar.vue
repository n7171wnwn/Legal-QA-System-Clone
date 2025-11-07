<template>
  <el-header class="navbar">
    <div class="navbar-container">
      <div class="navbar-brand">
        <img src="@/assets/logo.png" alt="Logo" class="logo" v-if="false">
        <span class="brand-text">智慧司法问答系统</span>
      </div>
      <el-menu
        :default-active="activeIndex"
        mode="horizontal"
        class="navbar-menu"
        @select="handleSelect"
      >
        <el-menu-item index="home">首页</el-menu-item>
        <el-menu-item index="chat">智能问答</el-menu-item>
        <el-menu-item index="knowledge">法律知识库</el-menu-item>
        <el-menu-item index="profile" v-if="isLoggedIn">个人中心</el-menu-item>
      </el-menu>
      <div class="navbar-actions">
        <el-button v-if="!isLoggedIn" type="text" @click="goToLogin">登录</el-button>
        <el-dropdown v-else>
          <span class="user-info">
            <i class="el-icon-user"></i>
            {{ userInfo.nickname || userInfo.username }}
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item @click.native="goToProfile">个人中心</el-dropdown-item>
            <el-dropdown-item @click.native="goToAdmin" v-if="isAdmin">管理后台</el-dropdown-item>
            <el-dropdown-item divided @click.native="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>
  </el-header>
</template>

<script>
export default {
  name: 'NavBar',
  computed: {
    activeIndex() {
      const routeName = this.$route.name
      if (routeName === 'Home') return 'home'
      if (routeName === 'Chat') return 'chat'
      if (routeName === 'Knowledge') return 'knowledge'
      if (routeName === 'Profile') return 'profile'
      return 'home'
    },
    isLoggedIn() {
      return this.$store.state.user.token
    },
    userInfo() {
      return this.$store.state.user.userInfo || {}
    },
    isAdmin() {
      return this.userInfo.userType === 1
    }
  },
  methods: {
    handleSelect(key) {
      const routeMap = {
        home: '/home',
        chat: '/chat',
        knowledge: '/knowledge',
        profile: '/profile'
      }
      if (routeMap[key]) {
        this.$router.push(routeMap[key])
      }
    },
    goToLogin() {
      this.$router.push('/login')
    },
    goToProfile() {
      this.$router.push('/profile')
    },
    goToAdmin() {
      this.$router.push('/admin/dashboard')
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
.navbar {
  background-color: var(--primary-color);
  color: white;
  padding: 0;
  height: 60px;
  line-height: 60px;
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.navbar-brand {
  display: flex;
  align-items: center;
  margin-right: 40px;
}

.logo {
  height: 40px;
  margin-right: 10px;
}

.brand-text {
  font-size: 20px;
  font-weight: bold;
  color: white;
}

.navbar-menu {
  flex: 1;
  background-color: transparent;
  border-bottom: none;
}

.navbar-menu .el-menu-item {
  color: rgba(255, 255, 255, 0.8);
  border-bottom: 2px solid transparent;
}

.navbar-menu .el-menu-item:hover,
.navbar-menu .el-menu-item.is-active {
  color: white;
  border-bottom-color: white;
  background-color: transparent;
}

.navbar-actions {
  margin-left: auto;
}

.user-info {
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.user-info i {
  margin-right: 5px;
}
</style>

