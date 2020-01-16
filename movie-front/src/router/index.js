import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Search from '@/views/Search'
import Detail from '@/views/Detail'
import MyPage from '@/views/MyPage'
import UserMovieList from '@/views/UserMovieList'
import UserWantList from '@/views/UserWantList'
import DiaryPage from '@/views/DiaryPage'
import Filmography from '@/views/Filmography'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/search/',
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
  },
  {
    path: '/user-movie-list/',
    name:'user-movie-list',
    component: UserMovieList
  },
  {
    path: '/user-want-list/',
    name:'user-want-list',
    component: UserWantList
  },
  {
    path: '/diarypage/',
    name: 'diarypage',
    component: DiaryPage
  },
  {
    path: '/filmography/',
    name: 'filmography',
    component: Filmography
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router