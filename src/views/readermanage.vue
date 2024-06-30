<template>
  <div>
    <el-table v-if="list" :data="list" stripe>
      <el-table-column align="center" label="ID" width="95">
        <template slot-scope="scope">
          {{ scope.$index }}
        </template>
      </el-table-column>
      <el-table-column label="借书卡号" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.CardID }}
        </template>
      </el-table-column>
      <el-table-column label="读者姓名" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.Name }}
        </template>
      </el-table-column>
      <el-table-column label="读者身份" width="110" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.Title }}</span>
        </template>
      </el-table-column>
      <el-table-column label="读者性别" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.Gender }}
        </template>
      </el-table-column>
      <el-table-column label="所在部门" width="200" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.Department }}</span>
        </template>
      </el-table-column>
      <el-table-column label="最大可借数量" width="200" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.MaxBorrowQuantity }}</span>
        </template>
      </el-table-column>
      <el-table-column label="已借数量" width="200" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.CurrentBorrowQuantity }}</span>
        </template>
      </el-table-column>
      <el-table-column label="电话号码" width="200" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.PhoneNumber }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" align="center">
        <template slot-scope="scope">
          <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleEdit(scope.row)">
            修改
          </el-button>
          <el-button class="filter-item" style="margin-left: 10px;" type="danger" icon="el-icon-delete" @click="handleDelete(scope.row.CardID)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-spinner v-if="listLoading" />

    <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
      添加用户
    </el-button>

    <!-- 用户对话框 -->
    <el-dialog :visible.sync="dialogVisible" :title="isEdit ? '编辑用户' : '添加用户'">
      <el-form :model="currentUser">
        <el-form-item label="卡号" :label-width="formLabelWidth">
          <el-input v-model="currentUser.CardID" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="姓名" :label-width="formLabelWidth">
          <el-input v-model="currentUser.Name" />
        </el-form-item>
        <el-form-item label="性别" :label-width="formLabelWidth">
          <el-select v-model="currentUser.Gender" placeholder="请选择">
            <el-option label="男" value="Male" />
            <el-option label="女" value="Female" />
            <el-option label="其他" value="Other" />
          </el-select>
        </el-form-item>
        <el-form-item label="身份" :label-width="formLabelWidth">
          <el-input v-model="currentUser.Title" />
        </el-form-item>
        <el-form-item label="最大借书量" :label-width="formLabelWidth">
          <el-input v-model="currentUser.MaxBorrowQuantity" type="number" />
        </el-form-item>
        <el-form-item label="部门" :label-width="formLabelWidth">
          <el-input v-model="currentUser.Department" />
        </el-form-item>
        <el-form-item label="电话号码" :label-width="formLabelWidth">
          <el-input v-model="currentUser.PhoneNumber" />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">{{ isEdit ? '更新' : '添加' }}</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { addReader, getReaderList, updateReader, deleteReader } from '@/api/table'

export default {
  data() {
    return {
      list: null,
      listLoading: true,
      dialogVisible: false,
      isEdit: false,
      currentUser: {
        CardID: '',
        Name: '',
        Gender: '',
        Title: '',
        MaxBorrowQuantity: '',
        CurrentBorrowQuantity: 0,
        Department: '',
        PhoneNumber: ''
      },
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
      console.log(searchParams)
      this.listLoading = true
      getReaderList(searchParams).then(response => {
        this.list = response.items
        this.listLoading = false
      }).catch(error => {
        this.$message.error('没有管理员权限')
      })
    },
    // 点击添加记录
    handleCreate() {
      this.dialogVisible = true
    },
    // 点击修改记录
    handleEdit(user) {
      this.isEdit = true
      this.currentUser = { ...user }
      this.dialogVisible = true
    },
    submitForm() {
      if (this.isEdit) {
        updateReader(this.currentUser).then(response => {
          this.$message({
            message: '用户信息更新成功',
            type: 'success'
          })
          this.dialogVisible = false
          this.fetchData()
        }).catch(error => {
          console.error('Error updating user:', error)
          this.$message.error('用户信息更新失败')
        })
      } else {
        addReader(this.currentUser).then(response => {
          this.$message({
            message: '用户添加成功',
            type: 'success'
          })
          this.dialogVisible = false
          this.fetchData()
        }).catch(error => {
          console.error('Error adding user:', error)
          this.$message.error('用户添加失败')
        })
      }
    },
    handleDelete(cardID) {
      this.$confirm('确定要删除该条记录吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteReader(cardID).then(response => {
          this.$message.success('删除记录成功')
          this.fetchData()
        }).catch(error => {
          console.error('Error deleting user:', error)
          this.$message.error('删除用户失败')
        })
      })
    }

  }
}
</script>
