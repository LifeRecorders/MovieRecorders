import Vue from 'vue'
import Vuex from 'vuex'
import jwtDecode from 'jwt-decode'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token: null,
    info: {
      movies: [],
      artists: [],
      users: [],
    },
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
      state.info.artists = []
      state.info.users = []
    },
    setMovieInfo(state, data) {
      state.info.movies.push(data)
    },
    setArtistInfo(state, data) {
      state.info.artists.push(data)
    },
    setUserInfo(state, data) {
      state.info.users.push(data)
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
    searchMovie(context, data) {
      context.commit('setMovieInfo', data)
    },
    searchArtist(context, data) {
      context.commit('setArtistInfo', data)
    },
    setUserInfo(context, data) {
      context.commit('setUserInfo', data)
    }
  }
})