<template>
  <div class="admin-qa">
    <div class="admin-content">
      <div class="content-header">
        <h2>问答管理</h2>
      </div>

      <div class="search-bar">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索问题..."
          style="width: 300px;"
          @keyup.enter.native="handleSearch"
        >
          <el-button slot="append" icon="el-icon-search" @click="handleSearch"></el-button>
        </el-input>
      </div>

      <el-table :data="qaList" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="question" label="问题" show-overflow-tooltip></el-table-column>
        <el-table-column prop="answer" label="答案" show-overflow-tooltip width="300"></el-table-column>
        <el-table-column prop="questionType" label="类型" width="120"></el-table-column>
        <el-table-column prop="confidenceScore" label="可信度" width="100">
          <template slot-scope="scope">
            <el-progress
              :percentage="scope.row.confidenceScore * 100"
              :color="getConfidenceColor(scope.row.confidenceScore)"
            ></el-progress>
          </template>
        </el-table-column>
        <el-table-column prop="feedbackType" label="反馈" width="100">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.feedbackType === 'positive'" type="success">正面</el-tag>
            <el-tag v-else-if="scope.row.feedbackType === 'negative'" type="danger">负面</el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="180">
          <template slot-scope="scope">
            {{ formatDate(scope.row.createTime) }}
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        @current-change="handlePageChange"
        :current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next"
        style="margin-top: 20px;"
      ></el-pagination>
    </div>
  </div>
</template>

<script>
import { getQARecords } from '@/api/api'

export default {
  name: 'AdminQA',
  data() {
    return {
      searchKeyword: '',
      qaList: [],
      page: 1,
      pageSize: 10,
      total: 0
    }
  },
  mounted() {
    this.loadData()
  },
  methods: {
    async loadData() {
      try {
        const response = await getQARecords({
          keyword: this.searchKeyword,
          page: this.page - 1,
          size: this.pageSize
        })
        this.qaList = response.data.content
        this.total = response.data.totalElements
      } catch (error) {
        this.$message.error('加载数据失败')
      }
    },
    handleSearch() {
      this.page = 1
      this.loadData()
    },
    handlePageChange(page) {
      this.page = page
      this.loadData()
    },
    getConfidenceColor(score) {
      if (score >= 0.8) return '#52c41a'
      if (score >= 0.6) return '#faad14'
      return '#f5222d'
    },
    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleString()
    }
  }
}
</script>

<style scoped>
.admin-qa {
  padding: 20px;
}

.admin-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
}

.content-header {
  margin-bottom: 20px;
}

.content-header h2 {
  margin: 0;
}

.search-bar {
  margin-bottom: 20px;
}
</style>

