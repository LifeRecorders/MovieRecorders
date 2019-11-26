<template>
  <div class="home">
    <h1>검색하기</h1>
    <div class="container col-6">
      <SearchBar v-on:searchInfo="searchInfo"/>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
// import { mapGetters } from 'vuex'
import SearchBar from '@/components/SearchBar'
import router from '@/router'

export default {
  name: 'Home',
  // computed: {
  //   ...mapGetters([
  //     'options',
  //   ])
  // },
  components: {
    SearchBar,
  },
  methods: {
    searchInfo(keyword) {
      const SERVER_IP = process.env.VUE_APP_SERVER_IP
      // const data = {
      //   keyword,
      // }
      // console.log(data)
      axios.get(`${SERVER_IP}/api/v1/search/?q=${keyword}`)
        .then(response => {
          console.log(response.data.movie)
          this.$store.dispatch('searchInfo', response.data)
        })
        .catch(error => {
          console.error(error)
        })
      // const movieData = {
      //   title: keyword,
      // }
      // const directorData = {
      //   name: keyword,
      // }
      // const actorData = {
      //   name: keyword,
      // }
      // const userData = {
      //   username: keyword,
      // }
      // axios.get(`${SERVER_IP}/api/~~~/`, movieData)
      //   .then(response => {
      //     this.$store.dispatch('searchMovie', response.data)
      //   })
      //   .catch(error => {
      //     console.error(error)
      //   })
      // axios.get(`${SERVER_IP}/api/~~~`, directorData)
      //   .then(response => {
      //     this.$store.dispatch('searchArtist', response.data)
      //   })
      //   .catch(error => {
      //     console.error(error)
      //   })
      // axios.get(`${SERVER_IP}/api/~~~`, actorData)
      //   .then(response => {
      //     this.$store.dispatch('searchArtist', response.data)
      //   })
      //   .catch(error => {
      //     console.error(error)
      //   })
      // axios.get(`${SERVER_IP}/api/~~~`, userData)
      //   .then(response => {
      //     this.$store.dispatch('searchUser', response.data)
      //   })
      //   .catch(error => {
      //     console.error(error)
      //   })
      // if(this.info.movies | this.info.artists | this.info.users) {
      //   router.push(`/search/${keyword}`)
      // }
      // this.$store.dispatch('searchMovie', keyword)
      router.push(`/search/${keyword}`)
    }
  }
}
</script>

<style>

</style>