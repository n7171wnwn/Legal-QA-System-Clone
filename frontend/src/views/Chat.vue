<template>
  <div class="chat">
    <NavBar />
    <div class="chat-container">
      <div class="chat-main">
        <div class="chat-messages" ref="messagesContainer">
          <div
            v-for="(message, index) in messages"
            :key="index"
            :class="['message', message.type]"
          >
            <div class="message-content" v-if="message.type === 'user'">
              <div class="message-bubble user-bubble">
                {{ message.content }}
              </div>
            </div>
            <div class="message-content" v-else>
              <div class="message-bubble bot-bubble">
                <div class="confidence-indicator" v-if="message.confidenceScore">
                  <span class="confidence-label">可信度：</span>
                  <el-progress
                    :percentage="message.confidenceScore * 100"
                    :color="getConfidenceColor(message.confidenceScore)"
                    :stroke-width="8"
                  ></el-progress>
                </div>
                <div class="answer-content" v-html="formatAnswer(message.answer)"></div>
                <div class="message-actions">
                  <el-button size="mini" icon="el-icon-thumb" @click="handleFeedback(message.id, 'positive')">有用</el-button>
                  <el-button size="mini" icon="el-icon-close" @click="handleFeedback(message.id, 'negative')">无用</el-button>
                  <el-button size="mini" icon="el-icon-star-off" @click="handleCollect(message)">收藏</el-button>
                </div>
              </div>
            </div>
          </div>
          <div v-if="loading" class="message bot">
            <div class="message-bubble bot-bubble">
              <i class="el-icon-loading"></i> 正在思考中...
            </div>
          </div>
        </div>
        <div class="chat-input-area">
          <el-input
            v-model="currentQuestion"
            type="textarea"
            :rows="3"
            placeholder="请输入您的问题..."
            @keyup.ctrl.enter.native="handleSend"
          ></el-input>
          <div class="input-actions">
            <el-button @click="handleSend" type="primary" :loading="loading">发送</el-button>
            <el-button @click="handleClear">清空</el-button>
          </div>
        </div>
      </div>
      <div class="chat-sidebar">
        <div class="sidebar-section">
          <h3>📚 参考法条</h3>
          <div v-if="currentRelatedLaws.length > 0">
            <div
              v-for="(law, index) in currentRelatedLaws"
              :key="index"
              class="law-item"
              @click="showLawDetail(law)"
            >
              {{ law.title }}<span v-if="formatArticleNumber(law.articleNumber)"> {{ formatArticleNumber(law.articleNumber) }}</span>
            </div>
          </div>
          <div v-else class="empty-state">暂无相关法条</div>
        </div>
        <div class="sidebar-section">
          <h3>⚖️ 相似案例</h3>
          <div v-if="currentRelatedCases.length > 0">
            <div
              v-for="(caseItem, index) in currentRelatedCases"
              :key="index"
              class="case-item"
              @click="showCaseDetail(caseItem)"
            >
              <div class="case-title">{{ caseItem.title }}</div>
              <div class="case-meta">{{ caseItem.courtName }} · {{ formatDate(caseItem.judgeDate) }}</div>
            </div>
          </div>
          <div v-else class="empty-state">暂无相关案例</div>
        </div>
        <div class="sidebar-section">
          <h3>🔍 识别实体</h3>
          <div v-if="currentEntities && Object.keys(currentEntities).length > 0">
            <div v-for="(items, key) in currentEntities" :key="key" v-if="items.length > 0">
              <div class="entity-label">{{ getEntityLabel(key) }}</div>
              <el-tag
                v-for="(item, idx) in items"
                :key="idx"
                size="mini"
                :type="getEntityTagType(key)"
                class="entity-tag"
              >
                {{ item }}
              </el-tag>
            </div>
          </div>
          <div v-else class="empty-state">暂无识别实体</div>
        </div>
      </div>
    </div>

    <el-dialog title="法条详情" :visible.sync="lawDialogVisible" width="60%">
      <div v-if="selectedLaw">
        <h3>{{ selectedLaw.title }}<span v-if="formatArticleNumber(selectedLaw.articleNumber)"> {{ formatArticleNumber(selectedLaw.articleNumber) }}</span></h3>
        <p>{{ selectedLaw.content }}</p>
      </div>
    </el-dialog>

    <el-dialog title="案例详情" :visible.sync="caseDialogVisible" width="60%">
      <div v-if="selectedCase">
        <h3>{{ selectedCase.title }}</h3>
        <p><strong>案由：</strong>{{ selectedCase.caseType }}</p>
        <p><strong>审理法院：</strong>{{ selectedCase.courtName }}</p>
        <p><strong>核心争议点：</strong>{{ selectedCase.disputePoint }}</p>
        <p><strong>判决结果：</strong>{{ selectedCase.judgmentResult }}</p>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import { askQuestion, submitFeedback } from '@/api/api'

export default {
  name: 'Chat',
  components: {
    NavBar
  },
  data() {
    return {
      currentQuestion: '',
      messages: [],
      loading: false,
      sessionId: 'session_' + Date.now(),
      currentRelatedLaws: [],
      currentRelatedCases: [],
      currentEntities: {},
      lawDialogVisible: false,
      caseDialogVisible: false,
      selectedLaw: null,
      selectedCase: null
    }
  },
  mounted() {
    if (this.$route.query.question) {
      this.currentQuestion = this.$route.query.question
      this.handleSend()
    }
  },
  methods: {
    async handleSend() {
      if (!this.currentQuestion.trim()) {
        this.$message.warning('请输入问题')
        return
      }

      const userMessage = {
        type: 'user',
        content: this.currentQuestion
      }
      this.messages.push(userMessage)

      const question = this.currentQuestion
      this.currentQuestion = ''
      this.loading = true

      try {
        const response = await askQuestion({
          question,
          sessionId: this.sessionId
        })

        const botMessage = {
          type: 'bot',
          content: response.data.answer,
          answer: response.data.answer,
          confidenceScore: response.data.confidenceScore,
          questionType: response.data.questionType,
          id: response.data.id
        }
        this.messages.push(botMessage)

        this.currentRelatedLaws = response.data.relatedLaws || []
        this.currentRelatedCases = response.data.relatedCases || []
        this.currentEntities = response.data.entities || {}

        this.$nextTick(() => {
          this.scrollToBottom()
        })
      } catch (error) {
        this.$message.error('提问失败：' + (error.message || '网络错误'))
      } finally {
        this.loading = false
      }
    },
    handleClear() {
      this.messages = []
      this.currentRelatedLaws = []
      this.currentRelatedCases = []
      this.currentEntities = {}
    },
    handleFeedback(qaId, type) {
      submitFeedback({
        qaId,
        feedbackType: type
      }).then(() => {
        this.$message.success('反馈提交成功，感谢您的反馈！')
      })
    },
    handleCollect(message) {
      this.$message.success('已收藏')
    },
    formatAnswer(answer) {
      if (!answer) return ''
      // 高亮法条引用
      return answer
        .replace(/《([^》]+)》/g, '<span class="law-highlight">《$1》</span>')
        .replace(/第(\d+)条/g, '<span class="article-highlight">第$1条</span>')
        .replace(/\n/g, '<br>')
    },
    getConfidenceColor(score) {
      if (score >= 0.8) return '#52c41a'
      if (score >= 0.6) return '#faad14'
      return '#f5222d'
    },
    showLawDetail(law) {
      this.selectedLaw = law
      this.lawDialogVisible = true
    },
    showCaseDetail(caseItem) {
      this.selectedCase = caseItem
      this.caseDialogVisible = true
    },
    getEntityLabel(key) {
      const labels = {
        laws: '法条',
        crimes: '罪名',
        organizations: '机构',
        concepts: '概念'
      }
      return labels[key] || key
    },
    getEntityTagType(key) {
      const types = {
        laws: 'primary',
        crimes: 'danger',
        organizations: 'warning',
        concepts: 'info'
      }
      return types[key] || ''
    },
    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString()
    },
    formatArticleNumber(articleNumber) {
      if (!articleNumber) return ''
      // 如果已经包含"第"和"条"，直接返回
      if (articleNumber.includes('第') && articleNumber.includes('条')) {
        return articleNumber
      }
      // 否则添加"第"和"条"
      return `第${articleNumber}条`
    },
    scrollToBottom() {
      const container = this.$refs.messagesContainer
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    }
  }
}
</script>

<style scoped>
.chat {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.chat-container {
  flex: 1;
  display: flex;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  padding: 20px;
  gap: 20px;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  min-height: 500px;
}

.message {
  margin-bottom: 20px;
}

.message-content {
  display: flex;
}

.message.user .message-content {
  justify-content: flex-end;
}

.message-bubble {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 8px;
  word-wrap: break-word;
}

.user-bubble {
  background: var(--primary-color);
  color: white;
}

.bot-bubble {
  background: #f5f5f5;
  color: #333;
}

.confidence-indicator {
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ddd;
}

.confidence-label {
  font-size: 12px;
  color: #666;
  margin-right: 10px;
}

.answer-content {
  line-height: 1.6;
}

.law-highlight {
  color: var(--primary-color);
  font-weight: bold;
}

.article-highlight {
  color: #faad14;
  font-weight: bold;
}

.message-actions {
  margin-top: 10px;
  display: flex;
  gap: 5px;
}

.chat-input-area {
  padding: 20px;
  border-top: 1px solid #eee;
}

.input-actions {
  margin-top: 10px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.chat-sidebar {
  width: 300px;
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  max-height: calc(100vh - 100px);
}

.sidebar-section {
  margin-bottom: 30px;
}

.sidebar-section h3 {
  font-size: 16px;
  color: #333;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 2px solid var(--primary-color);
}

.law-item,
.case-item {
  padding: 10px;
  margin-bottom: 8px;
  background: #f9f9f9;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.law-item:hover,
.case-item:hover {
  background: var(--secondary-color);
  color: var(--primary-color);
}

.case-title {
  font-weight: bold;
  margin-bottom: 5px;
}

.case-meta {
  font-size: 12px;
  color: #999;
}

.entity-label {
  font-size: 12px;
  color: #666;
  margin: 10px 0 5px 0;
}

.entity-tag {
  margin-right: 5px;
  margin-bottom: 5px;
}

.empty-state {
  color: #999;
  text-align: center;
  padding: 20px;
  font-size: 14px;
}
</style>

