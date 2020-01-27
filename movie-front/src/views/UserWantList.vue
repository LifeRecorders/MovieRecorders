<template>
  <div id="user-want-list" v-bind:style="{ backgroundImage: 'url(' + require('@/assets/images/backgroundcolor.png') +')'}">
    <header>
      <MovieHeader />
      <div id="searchBarDiv" class="container col-6 mt-5">
        <SearchBar id="searchBar" v-on:searchInfo="searchInfo"/>
      </div>
    </header>
    <div id="movie-list-body" class="container mt-5">
      <b-card-group deck>
        <div v-for="(movie, idx) in this.userWantList" v-bind:key="idx">
          <b-card
          border-variant="white"
          align="left"
          img-alt="Image"
          img-top
          tag="article"
          style="max-width: 10rem;"
          class="mb-2">
            <b-card-img rounded alt="Rounded image" class="mb-3" v-bind:src="movie.naver_big_poster_url" v-on:click="getDetail('movie', idx)">
            </b-card-img>
            <b-card-title>
              <h6>{{ movie.title }}</h6>
            </b-card-title>
            <b-card-text style="font-size:small;">
              <p>{{ getYear(movie.open_date) }} · {{ movie.nation }}</p>
            </b-card-text>
          </b-card>
        </div>
      </b-card-group>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapState } from 'vuex'
import router from '@/router'
import MovieHeader from '@/components/MovieHeader'
import SearchBar from '@/components/SearchBar'

export default {
  name: 'UserWantList',
    components: {
    MovieHeader,
    SearchBar
  },
  computed: {
    ...mapGetters([
      'options',
      'userId',
    ]),
    ...mapState([
      'user',
      'userWantList'
    ]),
    isLoggedIn() {
      return this.$store.getters.isLoggedIn;
    },
  },
  methods: {
    checkLoggedIn() {
      if(!this.isLoggedIn) {
        // 로그인 페이지로 보내겠다.
        router.push('/')
      }
    },
    getYear(date) {
      const year = date.substring(0, 4)
      return year
    },
    getDetail(type, idx) {
      let detailData
      let keyword
      detailData = this.userWantList[idx]
      keyword = this.userWantList[idx].title
      console.log(detailData)
      this.$store.dispatch('showDetail', detailData)
      router.push(`/detail/${keyword}`)
    },
  }

}
</script>

<style>
#movie-list-body {
  background: white;
}
#user-want-list > header {
  background-size: cover;
  height: 3rem;
  width: 100%;
  background-position-x: center;
}
#user-want-list #searchBarDiv {
  position: relative;
  top: -4.6rem;
}
</style>