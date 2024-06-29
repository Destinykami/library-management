import request from '@/utils/request'
// 获取书籍信息
export function getBookList(params) {
  return request({
    url: '/book/info',
    method: 'get',
    params
  })
}
// 获取读者信息
export function getReaderList(params) {
  return request({
    url: '/reader/info',
    method: 'get',
    params
  })
}
// 新增读者信息
export function addReader(data) {
  return request({
    url: '/reader/add',
    method: 'post',
    data
  })
}
// 新增书本
export function addBook(data) {
  return request({
    url: '/book/add',
    method: 'post',
    data
  })
}
// 删除书本
export function deleteBook(data) {
  return request({
    url: '/book/delete',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data
  })
}
// 修改书本
export function updateBook(data) {
  return request({
    url: '/book/update',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data
  })
}
// 修改读者
export function updateReader(data) {
  return request({
    url: '/reader/update',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data
  })
}
// 删除读者
export function deleteReader(data) {
  return request({
    url: '/reader/delete',
    method: 'post',
    headers: {
      'Content-Type': 'application/json'
    },
    data
  })
}
// 获取借书信息
export function getBorrowList(params) {
  return request({
    url: '/book/borrowinfo',
    method: 'get',
    params
  })
}
