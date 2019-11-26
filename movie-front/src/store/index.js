import Vue from 'vue'
import Vuex from 'vuex'
import jwtDecode from 'jwt-decode'

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
    }
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
    setDetail(state, data){
      state.detail = data
    }
  },
  actions: {
    login(context, token) {
      context.commit('setToken', token)
    },
    logout(context) {
      context.commit('setToken', null)
    },
    clearInfo(context) {
      context.commit('setClearInfo')
    },
    searchInfo(context, data) {
      context.commit('setInfo', data)
    },
    clearDetail(context) {
      context.commit('clearDetail')
    },
    showDetail(context, data) {
      context.commit('setDetail', data)
    },
  }
})