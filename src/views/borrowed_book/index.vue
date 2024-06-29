<template>
  <div>
    <el-button class="filter-item" type="primary" icon="el-icon-search" @click="fetchOverdueBooks">查询到期未归还图书</el-button>

    <el-table :data="overdueBooksList" stripe>
      <el-table-column label="图书编号" prop="ISBN" />
      <el-table-column label="书名" prop="Title" />
      <el-table-column label="读者姓名" prop="ReaderName" />
      <el-table-column label="借书证号码" prop="CardID" />
      <el-table-column label="借出日期" prop="BorrowDate" />
      <el-table-column label="到期日期" prop="DueDate" />
    </el-table>
  </div>
</template>

<script>
import { getOverdueBooks } from '@/api/table'

export default {
  data() {
    return {
      overdueBooksList: [],
      listLoading: false
    }
  },
  methods: {
    fetchOverdueBooks() {
      this.listLoading = true
      getOverdueBooks().then(response => {
        this.overdueBooksList = response.items
        this.listLoading = false
      }).catch(error => {
        console.error('Error fetching overdue books:', error)
        this.listLoading = false
      })
    }
  }
}
</script>
