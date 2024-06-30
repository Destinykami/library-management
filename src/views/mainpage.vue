<template>
  <div class="dashboard-container">
    <div class="header">
      <h1>图书管理系统@XMU</h1>
      <img src="../views/bg3.jpg" alt="Logo" class="logo">
      <!--      <h2>厦门大学计算机科学与技术系</h2>-->
    </div>
    <div class="content">
      <p>这是厦门大学计算机科学与技术系数据库系统原理课程设计。旨在通过该项目，提高对于数据库的掌握程度，以及增加前后端分离系统设计的经验。</p>
      <h3>系统功能：</h3>
      <ul>
        <li><strong>图书查询：</strong>支持按书名、ISBN、作者等多条件查询。</li>
        <li><strong>借书管理：</strong>便捷的借书操作和实时借书记录。</li>
        <li><strong>还书管理：</strong>轻松还书并计算超期罚款。</li>
        <li><strong>读者管理：</strong>管理读者信息及其借阅记录。</li>
        <li><strong>系统设置：</strong>管理员可对系统进行个性化配置。</li>
      </ul>
      <h3>项目介绍：</h3>
      <ul>
        <li><strong>前端：</strong>基于Vue-admin-template框架搭建，其提供了方便的权限管理功能</li>
        <li><strong>后端：</strong>基于Flask，相比与SpringBoot，学习路线比较平缓。</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardContainer',
  data() {
    return {
      name: '厦门大学计算机科学与技术系图书管理系统'
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
.dashboard-container {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 40px auto;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 20px;
}

.header h1 {
  font-size: 2.5em;
  margin: 0;
  color: #333;
}

.header h2 {
  font-size: 2em;
  margin: 0;
  color: #666;
}

.content {
  font-size: 1.2em;
  line-height: 1.6;
  color: #555;
}

.content h3 {
  font-size: 1.5em;
  margin-top: 20px;
  color: #333;
}

.content ul {
  list-style-type: disc;
  margin: 10px 0 20px 20px;
}

.content ul li {
  margin: 5px 0;
}

.content p {
  margin: 10px 0;
}
.logo {
  width: 600px;
  height: auto;
}
</style>
