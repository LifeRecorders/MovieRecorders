import Vue from 'vue'
import Vuex from 'vuex'
import jwtDecode from 'jwt-decode'
import axios from 'axios'
import router from '@/router'


Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token: null,
    info: {
      movies: [],
      directors: [],
      actors: [],
      users: [],
    },
    detail: [],
    user: [],
    userMovieList: [],
    diary: [],
  },
  getters: {
    isLoggedIn(state) {
      return state.token ? true : false
    },
    options(state) {
      return {
        headers: {
          Authorization: 'JWT ' + state.token
        }
      }
    },
    userId(state) {
      return state.token ? jwtDecode(state.token).user_id : null
    },
  },
  mutations: {
    setToken(state, token) {
      state.token = token
    },
    setClearInfo(state) {
      state.info.movies = []
      state.info.directors = []
      state.info.actors = []
      state.info.users = []
    },
    setInfo(state, data) {
      state.info.movies = data.movie
      state.info.directors = data.director
      state.info.actors = data.actor
      state.info.users = data.user
      console.log(state.info.movies)
      console.log(state.info.director)
    },
    clearDetail(state) {
      state.detail = []
    },
    setDetail(state, data) {
      state.detail = data
    },
    setUser(state, data) {
      state.user = data
    },
    clearUser(state) {
      state.user = []
    },
    setUserMovie(state, data) {
      state.userMovieList = data
    },
    clearUserMovie(state) {
      state.userMovieList = []
    },
    setDiary(state, data) {
      state.diary = data
    },
    clearDiary(state) {
      state.diary = []
    }
  },
  actions: {
    login(context, token) {
      context.commit('setToken', token)
    },
    logout(context) {
      context.commit('setToken', null)
    },
    searchInfo(context, keyword) {
      const SERVER_IP = process.env.VUE_APP_SERVER_IP
      console.log(keyword)

      axios.get(`${SERVER_IP}/api/v1/search/?q=${keyword}`)
        .then(response => {
          console.log(response)
          context.commit('setInfo', response.data)
          router.push(`/search/?q=${keyword}`)
        })
        .catch(error => {
          console.error(error)
        })
    },
    clearInfo(context) {
      context.commit('setClearInfo')
    },
    // setInfo(context, data) {
    //   context.commit('setInfo', data)
    // },
    clearDetail(context) {
      context.commit('clearDetail')
    },
    showDetail(context, data) {
      context.commit('setDetail', data)
    },
    setUser(context, data) {
      context.commit('setUser', data)
    },
    clearUser(context) {
      context.commit('clearUser')
    },
    setUserMovie(context, data) {
      context.commit('setUserMovie', data)
    },
    clearUserMovie(context) {
      context.commit('clearUserMovie')
    },
    setDiary(context, data) {
      context.commit('setDiary', data)
    },
    clearDiary(context) {
      context.commit('clearDiary')
    }
  }
})