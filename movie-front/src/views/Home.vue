<template>
  <div class="home">
    <header v-bind:style="{ backgroundImage: 'url(' + require('@/assets/images/maincolor.png') +')'}">
      <MovieHeader />
      <div id="searchBarDiv" class="container col-6 mt-5">
        <SearchBar id="searchBar" v-on:searchInfo="searchInfo"/>
      </div>
    </header>
  </div>
</template>

<script>
// import axios from 'axios'
// import { mapGetters } from 'vuex'
import MovieHeader from '@/components/MovieHeader'
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
    MovieHeader,
    SearchBar,
  },
  methods: {
    async searchInfo(keyword) {
      await this.$store.dispatch('searchInfo', keyword)
      router.push(`/search/${keyword}`)
    },
  }
}
</script>

<style>
.home > header {
  background-size: cover;
  height: 20rem;
  width: 100%;
  background-position-x: center;
}
.home #searchBarDiv {
  position: relative;
  top: 7rem;
}
</style>