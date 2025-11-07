<template>
  <div class="dashboard">
    <div class="dashboard-content">
      <el-row :gutter="20">
        <el-col :span="6" v-for="stat in stats" :key="stat.key">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon" :style="{ background: stat.color }">
                <i :class="stat.icon"></i>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ stat.value }}</div>
                <div class="stat-label">{{ stat.label }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" style="margin-top: 20px;">
        <el-col :span="12">
          <el-card>
            <div slot="header">问题分类统计</div>
            <div id="questionTypeChart" style="height: 300px;"></div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card>
            <div slot="header">热门问题TOP10</div>
            <el-table :data="hotQuestions" style="width: 100%">
              <el-table-column prop="question" label="问题" show-overflow-tooltip></el-table-column>
              <el-table-column prop="count" label="提问次数" width="100"></el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { getStats } from '@/api/api'
import * as echarts from 'echarts'

export default {
  name: 'Dashboard',
  data() {
    return {
      stats: [
        { key: 'today', label: '今日问答', value: 0, icon: 'el-icon-chat-line-round', color: '#1890ff' },
        { key: 'total', label: '总问答数', value: 0, icon: 'el-icon-document', color: '#52c41a' },
        { key: 'users', label: '用户数', value: 0, icon: 'el-icon-user', color: '#faad14' },
        { key: 'satisfaction', label: '满意度', value: '0%', icon: 'el-icon-star-on', color: '#f5222d' }
      ],
      hotQuestions: []
    }
  },
  mounted() {
    this.loadStats()
    this.initChart()
  },
  methods: {
    async loadStats() {
      try {
        const response = await getStats()
        const data = response.data
        this.stats[0].value = data.todayQuestions || 0
        // 这里可以根据实际API返回的数据更新其他统计值
      } catch (error) {
        this.$message.error('加载统计数据失败')
      }
    },
    initChart() {
      const chartDom = document.getElementById('questionTypeChart')
      if (!chartDom) return
      
      const myChart = echarts.init(chartDom)
      const option = {
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: '问题分类',
            type: 'pie',
            radius: '50%',
            data: [
              { value: 1048, name: '法条查询' },
              { value: 735, name: '概念定义' },
              { value: 580, name: '程序咨询' },
              { value: 484, name: '案例分析' }
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      myChart.setOption(option)
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.dashboard-content {
  max-width: 1400px;
  margin: 0 auto;
}

.stat-card {
  margin-bottom: 20px;
}

.stat-content {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
  margin-right: 20px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #999;
}
</style>

