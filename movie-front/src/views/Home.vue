<template>
  <div class="home">
    <header v-bind:style="{ backgroundImage: 'url(' + require('@/assets/images/maincolor.png') +')'}">
      <MovieHeader />
      <div id="searchBarDiv" class="container col-6 mt-5">
        <SearchBar id="searchBar" v-on:searchInfo="searchInfo"/>
      </div>
    </header>
    <br/>
    <br/>
    <h2>이런 영화는 어때요?</h2>
    <carousel-3d :width="200" :height="280">
      <div v-for="(movie, idx) in this.bestMovies" v-bind:key="idx">
        <slide v-bind:index="idx">
          <img v-bind:src="movie.naver_big_poster_url" alt="">
          <p>{{ movie.title }}</p>
        </slide>
      </div>
    </carousel-3d>
  </div>
</template>

<script>
import Vue from 'vue'
import Carousel3d from 'vue-carousel-3d'
// import axios from 'axios'
import { mapState } from 'vuex'
import MovieHeader from '@/components/MovieHeader'
import SearchBar from '@/components/SearchBar'
import router from '@/router'

Vue.use(Carousel3d)

export default {
  name: 'Home',
  computed: {
    ...mapState(['bestMovies'])
  },
  components: {
    MovieHeader,
    SearchBar,
  },
  methods: {
    async searchInfo(keyword) {
      await this.$store.dispatch('searchInfo', keyword)
      router.push(`/search/${keyword}`)
    },
    getBestMovies() {
      return this.$store.dispatch('setBestMovies')
    },
  },
  mounted() {
    this.getBestMovies()
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
carousel-3d {
  border-color: white;
  background-color: white;
}
</style>