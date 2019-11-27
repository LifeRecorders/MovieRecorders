import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Search from '@/views/Search'
import Detail from '@/views/Detail'
import MyPage from '@/views/MyPage'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/search/:keyword',
    name: 'search',
    component: Search
  },
  {
    path: '/detail/:keyword',
    name: 'detail',
    component: Detail
  },
  {
    path: '/mypage/',
    name: 'mypage',
    component: MyPage
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router