<template>
  <div>
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
          <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleEdit(scope.row)">
            修改
          </el-button>
          <el-button class="filter-item" style="margin-left: 10px;" type="danger" icon="el-icon-delete" @click="handleDelete(scope.row.ISBN)">
            删除
          </el-button>
        </template>
      </el-table-column>
      <el-spinner v-if="listLoading" />

    </el-table>
    <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
      添加图书
    </el-button>

    <!-- 添加图书对话框 -->
    <el-dialog :visible.sync="dialogVisible" title="添加图书">
      <el-form :model="newBook">
        <el-form-item label="ISBN" :label-width="formLabelWidth">
          <el-input v-model="newBook.ISBN" />
        </el-form-item>
        <el-form-item label="书名" :label-width="formLabelWidth">
          <el-input v-model="newBook.Title" />
        </el-form-item>
        <el-form-item label="出版社" :label-width="formLabelWidth">
          <el-input v-model="newBook.Publisher" />
        </el-form-item>
        <el-form-item label="作者" :label-width="formLabelWidth">
          <el-input v-model="newBook.Author" />
        </el-form-item>
        <el-form-item label="总数量" :label-width="formLabelWidth">
          <el-input v-model="newBook.TotalQuantity" type="number" />
        </el-form-item>
        <el-form-item label="可借数量" :label-width="formLabelWidth">
          <el-input v-model="newBook.AvailableQuantity" type="number" />
        </el-form-item>
        <el-form-item label="是否可借" :label-width="formLabelWidth">
          <el-switch v-model="newBook.IsAvailable" />
        </el-form-item>

      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitBookForm">确定</el-button>
      </span>
    </el-dialog>
    <!-- 编辑图书对话框 -->
    <el-dialog :visible.sync="editDialogVisible" title="编辑图书">
      <el-form :model="editBook">
        <el-form-item label="ISBN" :label-width="formLabelWidth">
          <el-input v-model="editBook.ISBN" disabled />
        </el-form-item>
        <el-form-item label="书名" :label-width="formLabelWidth">
          <el-input v-model="editBook.Title" />
        </el-form-item>
        <el-form-item label="出版社" :label-width="formLabelWidth">
          <el-input v-model="editBook.Publisher" />
        </el-form-item>
        <el-form-item label="作者" :label-width="formLabelWidth">
          <el-input v-model="editBook.Author" />
        </el-form-item>
        <el-form-item label="总数量" :label-width="formLabelWidth">
          <el-input v-model="editBook.TotalQuantity" type="number" />
        </el-form-item>
        <el-form-item label="可借数量" :label-width="formLabelWidth">
          <el-input v-model="editBook.AvailableQuantity" type="number" />
        </el-form-item>
        <el-form-item label="是否可借" :label-width="formLabelWidth">
          <el-switch v-model="editBook.IsAvailable" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitEditForm">确定</el-button>
      </span>
    </el-dialog>

  </div>
</template>

<script>
import { getBookList, addBook, deleteBook, updateBook } from '@/api/table'

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
      dialogVisible: false,
      editDialogVisible: false,
      newBook: {
        ISBN: '',
        Title: '',
        Publisher: '',
        Author: '',
        TotalQuantity: 0,
        AvailableQuantity: 0,
        IsAvailable: true
      },
      editBook: {
        ISBN: '',
        Title: '',
        Publisher: '',
        Author: '',
        TotalQuantity: 0,
        AvailableQuantity: 0,
        IsAvailable: true
      },
      isbn_to_delete: '',
      formLabelWidth: '120px'
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      const searchParams = {
        is_admin: this.$store.state.user.isAdmin
      }
      this.listLoading = true
      getBookList(searchParams).then(response => {
        this.list = response.items
        this.listLoading = false
      }).catch(error => {
        this.$message.error('没有管理员权限')
      })
    },
    handleCreate() {
      this.dialogVisible = true
    },
    // 修改记录
    handleEdit(book) {
      this.editBook = { ...book }
      this.editDialogVisible = true
    },

    // 删除记录
    handleDelete(isbn) {
      this.$confirm('确定要删除该条记录吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.isbn_to_delete = isbn
        deleteBook(this.isbn_to_delete).then(response => {
          this.$message.success('删除记录成功')
          this.fetchData()
        }).catch(error => {
          console.error('Error delete book:', error)
          this.$message.error('删除图书失败')
        })
      })
    },
    // 新增
    submitBookForm() {
      addBook(this.newBook).then(response => {
        this.$message({
          message: '图书添加成功',
          type: 'success'
        })
        this.dialogVisible = false
        this.fetchData()
      }).catch(error => {
        console.error('Error adding book:', error)
        this.$message.error('图书添加失败')
      })
    },
    // 修改
    submitEditForm() {
      updateBook(this.editBook).then(response => {
        this.$message({
          message: '图书信息更新成功',
          type: 'success'
        })
        this.editDialogVisible = false
        this.fetchData()
      }).catch(error => {
        console.error('Error updating book:', error)
        this.$message.error('图书信息更新失败')
      })
    }
  }
}
</script>
