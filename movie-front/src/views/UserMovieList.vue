<template>
  <div class="container mt-5">
    <b-card-group deck>
      <div v-for="(movie, idx) in this.userMovieList" v-bind:key="idx">
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
</template>

<script>
import { mapGetters, mapState } from 'vuex'
import router from '@/router'

export default {
  name: 'UserMovieList',
  computed: {
    ...mapGetters([
      'options',
      'userId',
    ]),
    ...mapState([
      'user',
      'userMovieList'
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
      detailData = this.userMovieList[idx]
      keyword = this.userMovieList[idx].title
      console.log(detailData)
      this.$store.dispatch('showDetail', detailData)
      router.push(`/detail/${keyword}`)
    },
  }

}
</script>

<style>

</style>