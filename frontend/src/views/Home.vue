<template>
  <div class="home">
    <NavBar />
    <div class="home-content">
      <div class="hero-section">
        <h1 class="hero-title">智慧司法问答系统</h1>
        <p class="hero-subtitle">基于AI技术的专业法律咨询服务</p>
        <div class="search-box">
          <el-input
            v-model="question"
            placeholder="请输入您的法律问题，例如：'劳动合同违约如何赔偿？'"
            size="large"
            @keyup.enter.native="handleAsk"
            class="question-input"
          >
            <el-button slot="append" icon="el-icon-search" @click="handleAsk">提问</el-button>
          </el-input>
          <div class="search-actions">
            <el-button icon="el-icon-microphone" circle></el-button>
            <el-button icon="el-icon-upload" circle></el-button>
          </div>
        </div>
      </div>

      <div class="quick-actions">
        <el-row :gutter="20">
          <el-col :span="6" v-for="action in quickActions" :key="action.key">
            <div class="action-card" @click="handleQuickAction(action)">
              <i :class="action.icon" class="action-icon"></i>
              <h3>{{ action.title }}</h3>
              <p>{{ action.desc }}</p>
            </div>
          </el-col>
        </el-row>
      </div>

      <div class="popular-questions">
        <h2>热门问题</h2>
        <el-row :gutter="20">
          <el-col :span="12" v-for="(q, index) in popularQuestions" :key="index">
            <div class="question-item" @click="handleQuestionClick(q)">
              <i class="el-icon-question"></i>
              <span>{{ q }}</span>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'

export default {
  name: 'Home',
  components: {
    NavBar
  },
  data() {
    return {
      question: '',
      quickActions: [
        {
          key: 'article',
          title: '法条查询',
          desc: '查询法律条文',
          icon: 'el-icon-document',
          route: '/knowledge?type=article'
        },
        {
          key: 'concept',
          title: '概念百科',
          desc: '法律概念定义',
          icon: 'el-icon-info',
          route: '/knowledge?type=concept'
        },
        {
          key: 'procedure',
          title: '程序指南',
          desc: '司法程序咨询',
          icon: 'el-icon-guide',
          route: '/chat'
        },
        {
          key: 'case',
          title: '案例参考',
          desc: '案例分析问答',
          icon: 'el-icon-folder-opened',
          route: '/knowledge?type=case'
        }
      ],
      popularQuestions: [
        '劳动合同违约如何赔偿？',
        '交通事故责任如何认定？',
        '离婚财产如何分割？',
        '欠款不还怎么办？',
        '工伤认定需要哪些材料？',
        '房屋买卖合同违约如何处理？'
      ]
    }
  },
  methods: {
    handleAsk() {
      if (!this.question.trim()) {
        this.$message.warning('请输入问题')
        return
      }
      this.$router.push({
        path: '/chat',
        query: { question: this.question }
      })
    },
    handleQuickAction(action) {
      this.$router.push(action.route)
    },
    handleQuestionClick(question) {
      this.$router.push({
        path: '/chat',
        query: { question }
      })
    }
  }
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(to bottom, var(--secondary-color), #f5f5f5);
}

.home-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.hero-section {
  text-align: center;
  padding: 60px 0;
}

.hero-title {
  font-size: 48px;
  color: var(--primary-color);
  margin-bottom: 20px;
  font-weight: bold;
}

.hero-subtitle {
  font-size: 20px;
  color: #666;
  margin-bottom: 40px;
}

.search-box {
  max-width: 800px;
  margin: 0 auto;
}

.question-input {
  margin-bottom: 20px;
}

.search-actions {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.quick-actions {
  margin: 60px 0;
}

.action-card {
  background: white;
  border-radius: 8px;
  padding: 30px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.action-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.action-icon {
  font-size: 48px;
  color: var(--primary-color);
  margin-bottom: 20px;
}

.action-card h3 {
  font-size: 20px;
  color: #333;
  margin-bottom: 10px;
}

.action-card p {
  color: #999;
  font-size: 14px;
}

.popular-questions {
  margin-top: 60px;
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.popular-questions h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
}

.question-item {
  padding: 15px;
  margin-bottom: 10px;
  background: #f9f9f9;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
}

.question-item:hover {
  background: var(--secondary-color);
  color: var(--primary-color);
}

.question-item i {
  margin-right: 10px;
  color: var(--primary-color);
}
</style>

