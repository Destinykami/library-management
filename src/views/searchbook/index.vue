<template>

  <div class="app-container">
    <!-- 搜索框和按钮 -->
    <el-input v-model="searchTitle" placeholder="按书名搜索" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
    <el-input v-model="searchISBN" placeholder="按ISBN搜索" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
    <el-input v-model="searchAuthor" placeholder="按作者搜索" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
    <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
      搜索
    </el-button>
    <el-table v-if="list" :data="list" stripe>
      <el-table-column align="center" label="ID" width="95">
        <template slot-scope="scope">
          {{ scope.$index }}
        </template>
      </el-table-column>
      <el-table-column label="书籍名称" width="300" align="center">
        <template slot-scope="scope">
          {{ scope.row.Title }}
        </template>
      </el-table-column>
      <el-table-column label="作者" width="200" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.Author }}</span>
        </template>
      </el-table-column>
      <el-table-column label="馆藏数量" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.TotalQuantity }}
        </template>
      </el-table-column>
      <el-table-column label="可借数量" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.AvailableQuantity }}
        </template>
      </el-table-column>
      <el-table-column label="ISBN" width="200" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.ISBN }}</span>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="Status" width="110" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.IsAvailable | statusFilter">{{ scope.row.IsAvailable ? '可借' : '不可借' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="操作" width="200" align="center">
        <template slot-scope="scope">
          <el-button type="success" size="small" @click="handleBorrow(scope.row.ISBN)">借阅图书</el-button>
        </template>
      </el-table-column>
      <el-spinner v-if="listLoading" />

    </el-table>
  </div>
</template>

<script>
import { borrowBook, searchBook } from '@/api/table'

export default {
  data() {
    return {
      list: null,
      listLoading: true,
      formLabelWidth: '120px',
      searchTitle: '',
      searchISBN: '',
      searchAuthor: '',
      isbn_to_borrow: '',
      reader_card_id: ''
    }
  },
  methods: {
    handleFilter() {
      this.listLoading = true
      const searchParams = {
        title: this.searchTitle,
        isbn: this.searchISBN,
        author: this.searchAuthor
      }
      searchBook(searchParams).then(response => {
        this.list = response.items
        this.listLoading = false
      }).catch(error => {
        console.error('Error searching books:', error)
        this.$message.error('搜索失败')
        this.listLoading = false
      })
    },
    handleBorrow(isbn) {
      this.$confirm('确定要借该书吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const currentUserCardID = this.$store.state.user.cardId
        this.isbn_to_borrow = isbn
        borrowBook(this.isbn_to_borrow, currentUserCardID).then(response => {
          this.$message.success('借书成功')
          this.handleFilter()
        }).catch(error => {
          console.error('Error borrow book:', error)
          this.$message.error('借书失败')
        })
      })
    }
  }
}
</script>
