<template>
  <div>
    <el-table v-if="list" :data="list" stripe>
      <el-table-column align="center" label="ID" width="95">
        <template slot-scope="scope">
          {{ scope.$index }}
        </template>
      </el-table-column>
      <el-table-column label="读者卡号" width="300" align="center">
        <template slot-scope="scope">
          {{ scope.row.CardID }}
        </template>
      </el-table-column>
      <el-table-column label="ISBN" width="200" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.ISBN }}</span>
        </template>
      </el-table-column>
      <el-table-column label="开始时间" width="200" align="center">
        <template slot-scope="scope">
          {{ scope.row.BorrowDate }}
        </template>
      </el-table-column>
      <el-table-column label="借书时长" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.BorrowPeriod }}
        </template>
      </el-table-column>
      <el-table-column label="还书时间" width="200" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.ReturnDate }}</span>
        </template>
      </el-table-column>
      <el-table-column label="罚款金额" width="200" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.Fine }}</span>
        </template>
      </el-table-column>
      <el-spinner v-if="listLoading" />
    </el-table>

  </div>
</template>

<script>
import { getBorrowList } from '@/api/table'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        '1': 'success',
        '0': 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      list: null,
      listLoading: true
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      getBorrowList().then(response => {
        this.list = response.items
        this.listLoading = false
      })
    }
  }
}
</script>
