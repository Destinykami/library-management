<template>
    <div class="app-container">
      <!-- 顶部功能 -->
      <div class="filter-container" style="margin-bottom: 15px">
        <!-- 一些按钮 -->
        <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
          搜索
        </el-button>

      </div>
  
      <!--数据表格-->
      <el-table
          ref="multipleTable"
          :data="tableData"
          border
          style="width: 100%">
        <el-table-column
            fixed
            type="selection"
            width="55">
        </el-table-column>
        <el-table-column
            fixed
            prop="borrowid"
            label="序号"
            width="100">
        </el-table-column>
        <el-table-column
            prop="username"
            label="用户名"
            show-overflow-tooltip>
        </el-table-column>
        <el-table-column
            prop="bookname"
            label="图书名"
            show-overflow-tooltip>
        </el-table-column>
        <el-table-column
            prop="borrowtimestr"
            label="借书时间">
        </el-table-column>
        <el-table-column
            label="还书时间">
            <template slot-scope="scope">
              <span v-if="scope.row.returntimestr === null || scope.row.returntimestr === ''" style="color: red">等待还书</span>
              <span v-else style="color: #1aac1a">{{scope.row.returntimestr}}</span>
            </template>
        </el-table-column>
        <el-table-column
            fixed="right"
            label="操作"
            :width="roleIsAdmin?'180px':'110px'">
          <template slot-scope="scope">
            <el-button v-permission="['admin']" @click="handleDelete(scope.row,scope.$index)" type="danger" size="small">删除</el-button>
            <el-button @click="handleReturn(scope.row,scope.$index)" type="success" size="small">归还图书</el-button>
          </template>
        </el-table-column>
      </el-table>
  
    </div>
  </template>