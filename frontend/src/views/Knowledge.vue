<template>
  <div class="knowledge">
    <NavBar />
    <div class="knowledge-container">
      <div class="knowledge-header">
        <h1>法律知识库</h1>
        <div class="search-bar">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索法条、案例、概念..."
            size="large"
            @keyup.enter.native="handleSearch"
          >
            <el-button slot="append" icon="el-icon-search" @click="handleSearch">搜索</el-button>
          </el-input>
        </div>
        <div class="filter-tabs">
          <el-radio-group v-model="activeTab" @change="handleTabChange">
            <el-radio-button label="article">法条</el-radio-button>
            <el-radio-button label="case">案例</el-radio-button>
            <el-radio-button label="concept">概念</el-radio-button>
          </el-radio-group>
        </div>
      </div>

      <div class="knowledge-content">
        <!-- 法条列表 -->
        <div v-if="activeTab === 'article'" class="article-list">
          <el-card
            v-for="article in articles"
            :key="article.id"
            class="article-card"
            @click.native="showArticleDetail(article)"
          >
            <div class="article-header">
              <h3>{{ article.title }}</h3>
              <el-tag size="small">{{ article.lawType }}</el-tag>
            </div>
            <p class="article-number" v-if="formatArticleNumber(article.articleNumber)">{{ formatArticleNumber(article.articleNumber) }}</p>
            <p class="article-content">{{ article.content }}</p>
            <div class="article-footer">
              <span class="article-org">{{ article.publishOrg }}</span>
              <span class="article-date">{{ formatDate(article.publishDate) }}</span>
            </div>
          </el-card>
          <el-pagination
            v-if="articleTotal > 0"
            @current-change="handleArticlePageChange"
            :current-page="articlePage"
            :page-size="articlePageSize"
            :total="articleTotal"
            layout="total, prev, pager, next"
          ></el-pagination>
        </div>

        <!-- 案例列表 -->
        <div v-if="activeTab === 'case'" class="case-list">
          <el-card
            v-for="caseItem in cases"
            :key="caseItem.id"
            class="case-card"
            @click.native="showCaseDetail(caseItem)"
          >
            <div class="case-header">
              <h3>{{ caseItem.title }}</h3>
              <el-tag size="small" type="warning">{{ caseItem.caseType }}</el-tag>
            </div>
            <p class="case-court">{{ caseItem.courtName }}</p>
            <p class="case-point">{{ caseItem.disputePoint }}</p>
            <div class="case-footer">
              <span>判决日期：{{ formatDate(caseItem.judgeDate) }}</span>
            </div>
          </el-card>
          <el-pagination
            v-if="caseTotal > 0"
            @current-change="handleCasePageChange"
            :current-page="casePage"
            :page-size="casePageSize"
            :total="caseTotal"
            layout="total, prev, pager, next"
          ></el-pagination>
        </div>

        <!-- 概念列表 -->
        <div v-if="activeTab === 'concept'" class="concept-list">
          <el-card
            v-for="concept in concepts"
            :key="concept.id"
            class="concept-card"
            @click.native="showConceptDetail(concept)"
          >
            <h3>{{ concept.name }}</h3>
            <p class="concept-definition">{{ concept.definition }}</p>
            <el-tag size="small">{{ concept.lawType }}</el-tag>
          </el-card>
          <el-pagination
            v-if="conceptTotal > 0"
            @current-change="handleConceptPageChange"
            :current-page="conceptPage"
            :page-size="conceptPageSize"
            :total="conceptTotal"
            layout="total, prev, pager, next"
          ></el-pagination>
        </div>
      </div>
    </div>

    <!-- 详情对话框 -->
    <el-dialog
      :title="detailTitle"
      :visible.sync="detailVisible"
      width="60%"
    >
      <div v-if="selectedItem">
        <div v-if="activeTab === 'article'">
          <h3>{{ selectedItem.title }}<span v-if="formatArticleNumber(selectedItem.articleNumber)"> {{ formatArticleNumber(selectedItem.articleNumber) }}</span></h3>
          <p>{{ selectedItem.content }}</p>
          <p><strong>发布机构：</strong>{{ selectedItem.publishOrg || '未知' }}</p>
          <p><strong>发布日期：</strong>{{ formatDate(selectedItem.publishDate) || '未知' }}</p>
        </div>
        <div v-if="activeTab === 'case'">
          <h3>{{ selectedItem.title }}</h3>
          <p><strong>案由：</strong>{{ selectedItem.caseType }}</p>
          <p><strong>审理法院：</strong>{{ selectedItem.courtName }}</p>
          <p><strong>核心争议点：</strong>{{ selectedItem.disputePoint }}</p>
          <p><strong>判决结果：</strong>{{ selectedItem.judgmentResult }}</p>
          <p><strong>案例内容：</strong>{{ selectedItem.content }}</p>
        </div>
        <div v-if="activeTab === 'concept'">
          <h3>{{ selectedItem.name }}</h3>
          <p><strong>定义：</strong>{{ selectedItem.definition }}</p>
          <p><strong>详细解释：</strong>{{ selectedItem.explanation }}</p>
          <p><strong>所属领域：</strong>{{ selectedItem.lawType }}</p>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import { searchArticles, searchCases, searchConcepts } from '@/api/api'

export default {
  name: 'Knowledge',
  components: {
    NavBar
  },
  data() {
    return {
      searchKeyword: '',
      activeTab: 'article',
      articles: [],
      cases: [],
      concepts: [],
      articlePage: 1,
      articlePageSize: 10,
      articleTotal: 0,
      casePage: 1,
      casePageSize: 10,
      caseTotal: 0,
      conceptPage: 1,
      conceptPageSize: 10,
      conceptTotal: 0,
      detailVisible: false,
      selectedItem: null,
      detailTitle: ''
    }
  },
  mounted() {
    const type = this.$route.query.type
    if (type) {
      this.activeTab = type
    }
    this.loadData()
  },
  methods: {
    handleSearch() {
      this.loadData()
    },
    handleTabChange() {
      this.loadData()
    },
    async loadData() {
      if (this.activeTab === 'article') {
        await this.loadArticles()
      } else if (this.activeTab === 'case') {
        await this.loadCases()
      } else if (this.activeTab === 'concept') {
        await this.loadConcepts()
      }
    },
    async loadArticles() {
      try {
        const response = await searchArticles({
          keyword: this.searchKeyword || '',
          page: this.articlePage - 1,
          size: this.articlePageSize
        })
        this.articles = response.data.content
        this.articleTotal = response.data.totalElements
      } catch (error) {
        this.$message.error('加载法条失败')
      }
    },
    async loadCases() {
      try {
        const response = await searchCases({
          keyword: this.searchKeyword || '',
          page: this.casePage - 1,
          size: this.casePageSize
        })
        this.cases = response.data.content
        this.caseTotal = response.data.totalElements
      } catch (error) {
        this.$message.error('加载案例失败')
      }
    },
    async loadConcepts() {
      try {
        const response = await searchConcepts({
          keyword: this.searchKeyword || '',
          page: this.conceptPage - 1,
          size: this.conceptPageSize
        })
        this.concepts = response.data.content
        this.conceptTotal = response.data.totalElements
      } catch (error) {
        this.$message.error('加载概念失败')
      }
    },
    handleArticlePageChange(page) {
      this.articlePage = page
      this.loadArticles()
    },
    handleCasePageChange(page) {
      this.casePage = page
      this.loadCases()
    },
    handleConceptPageChange(page) {
      this.conceptPage = page
      this.loadConcepts()
    },
    showArticleDetail(article) {
      this.selectedItem = article
      this.detailTitle = '法条详情'
      this.detailVisible = true
    },
    showCaseDetail(caseItem) {
      this.selectedItem = caseItem
      this.detailTitle = '案例详情'
      this.detailVisible = true
    },
    showConceptDetail(concept) {
      this.selectedItem = concept
      this.detailTitle = '概念详情'
      this.detailVisible = true
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
    }
  }
}
</script>

<style scoped>
.knowledge {
  min-height: 100vh;
  background: #f5f5f5;
}

.knowledge-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.knowledge-header {
  background: white;
  padding: 30px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.knowledge-header h1 {
  font-size: 32px;
  color: var(--primary-color);
  margin-bottom: 20px;
}

.search-bar {
  margin-bottom: 20px;
}

.filter-tabs {
  margin-top: 20px;
}

.knowledge-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.article-card,
.case-card,
.concept-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.article-card:hover,
.case-card:hover,
.concept-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.article-header,
.case-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.article-header h3,
.case-header h3 {
  margin: 0;
  color: #333;
}

.article-number {
  color: var(--primary-color);
  font-weight: bold;
  margin: 10px 0;
}

.article-content {
  color: #666;
  line-height: 1.6;
  margin: 10px 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
  font-size: 12px;
  color: #999;
}

.case-court {
  color: #666;
  margin: 10px 0;
}

.case-point {
  color: #666;
  line-height: 1.6;
  margin: 10px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.case-footer {
  margin-top: 10px;
  font-size: 12px;
  color: #999;
}

.concept-card h3 {
  color: var(--primary-color);
  margin-bottom: 10px;
}

.concept-definition {
  color: #666;
  line-height: 1.6;
  margin: 10px 0;
}
</style>

