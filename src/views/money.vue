<template>
  <div>
    <el-button class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">查询欠款</el-button>

    <el-table :data="overdueBooksList" stripe v-loading="listLoading">
      <el-table-column label="借书证号码" prop="CardID" />
      <el-table-column label="读者姓名" prop="Name" />
      <el-table-column label="部门" prop="Department" />
      <el-table-column label="电话号码" prop="PhoneNumber" />
      <el-table-column label="欠款金额" prop="Fine" />
      <el-table-column label="操作" width="200" align="center">
        <template slot-scope="scope">
          <template v-if="scope.row.Fine > 0">
            <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleReturnMoney(scope.row.CardID)">
              缴纳欠款
            </el-button>
          </template>
          <template v-else>
            <span>您没有欠款，无需缴纳</span>
          </template>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { returnMoney, getdebt } from '@/api/table'

export default {
  data() {
    return {
      overdueBooksList: [],
      listLoading: false
    }
  },
  methods: {
    handleFilter() {
      this.listLoading = true
      const searchParams = {
        cardid: this.$store.state.user.cardId
      }
      getdebt(searchParams).then(response => {
        console.log(response)
        this.overdueBooksList = response.items
        this.listLoading = false
      }).catch(error => {
        console.error('Error searching:', error)
        this.$message.error('搜索失败')
        this.listLoading = false
      })
    },
    handleReturnMoney(cardID) {
      this.$confirm('确定要缴纳欠款吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        returnMoney(cardID).then(response => {
          this.$message.success('缴纳成功')
          this.handleFilter()
        }).catch(_ => {
          this.$message.error('缴纳失败')
        })
      })
    }
  }
}
</script>
