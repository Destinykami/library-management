import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: '主界面',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '图书管理系统', icon: 'education' }
    }]
  },

  {
    path: '/admin',
    component: Layout,
    redirect: '/admin/reader_info',
    name: '管理员模块',
    meta: { title: '管理员模块', icon: 'el-icon-s-help' },
    children: [
      {
        path: 'reader_info',
        name: 'reader_info',
        component: () => import('@/views/readermanage/index'),
        meta: { title: '读者信息管理', icon: 'peoples' }
      },
      {
        path: 'book_info',
        name: 'book_info',
        component: () => import('@/views/bookinfo/index'),
        meta: { title: '书籍管理', icon: 'documentation' }
      }
    ]
  },

  {
    path: '/borrow_info',
    component: Layout,
    children: [
      {
        path: 'borrow_info',
        name: 'borrow_info',
        component: () => import('@/views/borrowinfo/index'),
        meta: { title: '借阅信息', icon: 'eye-open' }
      }
    ]
  },
  {
    path: '/return_and_borrow',
    component: Layout,
    meta: { title: '查书&借书&还书系统', icon: 'form' },
    children: [
      {
        path: 'borrow',
        name: 'borrow',
        component: () => import('@/views/searchbook/index'),
        meta: { title: '借书&查书系统', icon: 'form' }
      },
      {
        path: 'return',
        name: 'return',
        component: () => import('@/views/returnbook/index'),
        meta: { title: '还书系统', icon: 'form' }
      }
    ]
  },
  {
    path: '/reader_info_and_borrowed_book',
    component: Layout,
    children: [
      {
        path: 'reader_info_and_borrowed_book',
        name: 'reader_info_and_borrowed_book',
        component: () => import('@/views/reader_info_and_borrowed_book/index'),
        meta: { title: '读者已借书信息', icon: 'table' }
      }
    ]
  },
  {
    path: '/borrowed_book',
    component: Layout,
    children: [
      {
        path: 'borrowed_book',
        name: 'borrowed_book',
        component: () => import('@/views/borrowed_book/index'),
        meta: { title: '已借未归还图书', icon: 'search' }
      }
    ]
  },
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
