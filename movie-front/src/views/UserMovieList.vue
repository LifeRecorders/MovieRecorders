<template>
  <div class="container mt-5">
    
    <b-card-group deck>
      <div v-for="(movie, idx) in this.userMovieList" v-bind:key="idx">
        <b-card 
        v-bind:title="movie" 
        img-src="https://picsum.photos/300/300/?image=51" 
        img-alt="Image" 
        img-top
        align="left"
        style="max-width: 8rem;">
          <b-card-text>
            .
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
  }

}
</script>

<style>

</style>