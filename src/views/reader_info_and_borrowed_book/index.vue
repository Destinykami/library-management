<template>
  <div class="app-container">
    <h1>读者信息查询：</h1>

    <!-- 搜索框和按钮 -->
    <el-input v-model="searchName" placeholder="搜索读者名" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
    <el-input v-model="searchCardID" placeholder="搜索读者卡号" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
    <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
      搜索
    </el-button>
    <el-table v-if="list" :data="list" stripe>
      <el-table-column align="center" label="ID" width="95">
        <template slot-scope="scope">
          {{ scope.$index }}
        </template>
      </el-table-column>
      <el-table-column label="读者名称" width="300" align="center">
        <template slot-scope="scope">
          {{ scope.row.Name }}
        </template>
      </el-table-column>
      <el-table-column label="图书编号" width="200" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.ISBN }}</span>
        </template>
      </el-table-column>
      <el-table-column label="书名" width="300" align="center">
        <template slot-scope="scope">
          {{ scope.row.BookName }}
        </template>
      </el-table-column>
      <el-spinner v-if="listLoading" />

    </el-table>
  </div>
</template>

<script>
import { borrowBook, searchReaderAndBook } from '@/api/table'

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
        name: this.searchName,
        cardid: this.searchCardID,
      }
      searchReaderAndBook(searchParams).then(response => {
        console.log(response)
        this.list = response.items
        this.listLoading = false
      }).catch(error => {
        console.error('Error searching :', error)
        this.$message.error('搜索失败')
        this.listLoading = false
      })
    }
  }
}
</script>
