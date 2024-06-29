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
        <el-spinner v-if="listLoading" />

        </el-table>
        <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        添加图书
      </el-button>

        <!-- 添加图书对话框 -->
    <el-dialog :visible.sync="dialogVisible" title="添加图书">
      <el-form :model="newBook">
        <el-form-item label="ISBN" :label-width="formLabelWidth">
          <el-input v-model="newBook.ISBN"></el-input>
        </el-form-item>
        <el-form-item label="书名" :label-width="formLabelWidth">
          <el-input v-model="newBook.Title"></el-input>
        </el-form-item>
        <el-form-item label="出版社" :label-width="formLabelWidth">
          <el-input v-model="newBook.Publisher"></el-input>
        </el-form-item>
        <el-form-item label="作者" :label-width="formLabelWidth">
          <el-input v-model="newBook.Author"></el-input>
        </el-form-item>
        <el-form-item label="总数量" :label-width="formLabelWidth">
          <el-input v-model="newBook.TotalQuantity" type="number"></el-input>
        </el-form-item>
        <el-form-item label="可借数量" :label-width="formLabelWidth">
          <el-input v-model="newBook.AvailableQuantity" type="number"></el-input>
        </el-form-item>

        <!-- TODO  这里新增触发器 -->
        <el-form-item label="是否可借" :label-width="formLabelWidth">
          <el-switch v-model="newBook.IsAvailable"></el-switch>
        </el-form-item>
        
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitBookForm">确定</el-button>
      </span>
    </el-dialog>

    </div>
</template>

<script>
import { getBookList ,addBook} from '@/api/table'

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
            newBook: {
                ISBN: '',
                Title: '',
                Publisher: '',
                Author: '',
                TotalQuantity: 0,
                AvailableQuantity: 0,
                IsAvailable: true
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
            getBookList().then(response => {
                this.list = response.items
                this.listLoading = false
            })
        },
        handleCreate() {
            this.dialogVisible = true
        },
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
        }
    }
}
</script>