<template>
  <div class="login">
    <div class="login-container">
      <div class="login-card">
        <h1>智慧司法问答系统</h1>
        <el-tabs v-model="activeTab">
          <el-tab-pane label="登录" name="login">
            <el-form :model="loginForm" :rules="loginRules" ref="loginForm">
              <el-form-item prop="username">
                <el-input v-model="loginForm.username" placeholder="用户名" prefix-icon="el-icon-user"></el-input>
              </el-form-item>
              <el-form-item prop="password">
                <el-input v-model="loginForm.password" type="password" placeholder="密码" prefix-icon="el-icon-lock" @keyup.enter.native="handleLogin"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" style="width: 100%" @click="handleLogin" :loading="loading">登录</el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="注册" name="register">
            <el-form :model="registerForm" :rules="registerRules" ref="registerForm">
              <el-form-item prop="username">
                <el-input v-model="registerForm.username" placeholder="用户名" prefix-icon="el-icon-user"></el-input>
              </el-form-item>
              <el-form-item prop="password">
                <el-input v-model="registerForm.password" type="password" placeholder="密码" prefix-icon="el-icon-lock"></el-input>
              </el-form-item>
              <el-form-item prop="email">
                <el-input v-model="registerForm.email" placeholder="邮箱" prefix-icon="el-icon-message"></el-input>
              </el-form-item>
              <el-form-item prop="phone">
                <el-input v-model="registerForm.phone" placeholder="手机号" prefix-icon="el-icon-phone"></el-input>
              </el-form-item>
              <el-form-item prop="nickname">
                <el-input v-model="registerForm.nickname" placeholder="昵称" prefix-icon="el-icon-user"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" style="width: 100%" @click="handleRegister" :loading="loading">注册</el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      activeTab: 'login',
      loading: false,
      loginForm: {
        username: '',
        password: ''
      },
      registerForm: {
        username: '',
        password: '',
        email: '',
        phone: '',
        nickname: ''
      },
      loginRules: {
        username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
      },
      registerRules: {
        username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
        email: [{ type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }],
        phone: [{ pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }],
        nickname: [{ required: true, message: '请输入昵称', trigger: 'blur' }]
      }
    }
  },
  methods: {
    async handleLogin() {
      this.$refs.loginForm.validate(async (valid) => {
        if (valid) {
          this.loading = true
          try {
            await this.$store.dispatch('user/login', this.loginForm)
            this.$message.success('登录成功')
            const redirect = this.$route.query.redirect || '/home'
            this.$router.push(redirect)
          } catch (error) {
            this.$message.error('登录失败：' + (error.message || '用户名或密码错误'))
          } finally {
            this.loading = false
          }
        }
      })
    },
    async handleRegister() {
      this.$refs.registerForm.validate(async (valid) => {
        if (valid) {
          this.loading = true
          try {
            await this.$store.dispatch('user/register', this.registerForm)
            this.$message.success('注册成功')
            const redirect = this.$route.query.redirect || '/home'
            this.$router.push(redirect)
          } catch (error) {
            this.$message.error('注册失败：' + (error.message || '注册信息有误'))
          } finally {
            this.loading = false
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.login {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--primary-color) 0%, #4a90e2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-container {
  width: 100%;
  max-width: 400px;
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 8px;
  padding: 40px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.login-card h1 {
  text-align: center;
  color: var(--primary-color);
  margin-bottom: 30px;
  font-size: 28px;
}
</style>

