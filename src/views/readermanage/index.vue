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
      </el-table>
      <el-spinner v-if="listLoading" />

      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        添加用户
      </el-button>

       <!-- 添加用户对话框 -->
    <el-dialog :visible.sync="dialogVisible" title="添加用户">
      <el-form :model="newUser">
        <el-form-item label="卡号" :label-width="formLabelWidth">
          <el-input v-model="newUser.CardID"></el-input>
        </el-form-item>
        <el-form-item label="姓名" :label-width="formLabelWidth">
          <el-input v-model="newUser.Name"></el-input>
        </el-form-item>
        <el-form-item label="性别" :label-width="formLabelWidth">
          <el-select v-model="newUser.Gender" placeholder="请选择">
            <el-option label="男" value="Male"></el-option>
            <el-option label="女" value="Female"></el-option>
            <el-option label="其他" value="Other"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="身份" :label-width="formLabelWidth">
          <el-input v-model="newUser.Title"></el-input>
        </el-form-item>
        <el-form-item label="最大借书量" :label-width="formLabelWidth">
          <el-input v-model="newUser.MaxBorrowQuantity" type="number"></el-input>
        </el-form-item>
        <el-form-item label="部门" :label-width="formLabelWidth">
          <el-input v-model="newUser.Department"></el-input>
        </el-form-item>
        <el-form-item label="电话号码" :label-width="formLabelWidth">
          <el-input v-model="newUser.PhoneNumber"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { addReader, getReaderList } from '@/api/table'

export default {
  // filters: {
  //     statusFilter(status) {
  //         const statusMap = {
  //             '1': 'success',
  //             '0': 'danger'
  //         }
  //         return statusMap[1]
  //     }
  // },
  data() {
      return {
          list: null,
          listLoading: true,
          dialogVisible: false,
          newUser: {
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
          this.listLoading = true
          getReaderList().then(response => {
              this.list = response.items
              this.listLoading = false
          })
      },
      // 点击添加记录
      handleCreate() {
        this.dialogVisible = true
    },
    submitForm() {
      addReader(this.newUser).then(response => {
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

  }
}
</script>