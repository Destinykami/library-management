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
<!--      <el-table-column label="还书时间" width="200" align="center">-->
<!--        <template slot-scope="scope">-->
<!--          <span>{{ scope.row.ReturnDate }}</span>-->
<!--        </template>-->
<!--      </el-table-column>-->
      <el-table-column label="罚款金额" width="200" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.Fine }}</span>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="操作" width="200" align="center">
        <template slot-scope="scope">
          <el-button type="success" size="small" @click="handleReturn(scope.row.ISBN)">归还图书</el-button>
        </template>
      </el-table-column>
      <el-spinner v-if="listLoading" />
    </el-table>

  </div>
</template>

<script>
import { returnBook, getBorrowListOfOne } from '@/api/table'

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
      listLoading: true,
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      const searchParams = {
        card_id:this.$store.state.user.cardId
      }
      getBorrowListOfOne(searchParams).then(response => {
        this.list = response.items
        this.listLoading = false
      })
    },
    handleReturn(isbn) {
      this.$confirm('确定要还该书吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const currentUserCardID = this.$store.state.user.cardId
        this.isbn_to_borrow = isbn
        returnBook(this.isbn_to_borrow, currentUserCardID).then(response => {
          this.$message.success('还书成功')
          this.fetchData()
        }).catch(error => {
          console.error('Error return book:', error)
          this.$message.error('还书失败')
        })
      })
    }
  }
}
</script>
