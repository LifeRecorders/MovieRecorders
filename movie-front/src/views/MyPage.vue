<template>
  <div class="container mt-5 text-left">
    <h2>{{ this.user.username }}</h2>
    <br/>
    <router-link to="/user-movie-list/" id="router-movie-list">
      <h6>내가 본 영화 {{ this.userMovieList.length }} </h6>
    </router-link>
    <h6>앞으로 볼 영화 </h6>
    <br/>
    <hr/>
    <DiaryCalendar v-on:openDiary="openDiary" />
  </div>
</template>

<script>
import { mapGetters, mapState } from 'vuex'
import router from '@/router'
import axios from 'axios'
import DiaryCalendar from '@/components/DiaryCalendar'


export default {
  name: "MyPage",
  // data () {
  //   return {
  //     user: [],
  //     userMovie: []
  //   }
  // },
  components: {
    DiaryCalendar
  },
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
    getUserInfo() {
      this.$store.dispatch('clearUser')
      const SERVER_IP = process.env.VUE_APP_SERVER_IP

      axios.get(`${SERVER_IP}/accounts/users/${this.userId}`, this.options)
        .then(response => {
          this.$store.dispatch('setUser', response.data)
        })
        .then(error => {
          console.error(error)
        })
    },
    getUserMovie() {
      this.$store.dispatch('clearUserMovie')
      const SERVER_IP = process.env.VUE_APP_SERVER_IP

      axios.get(`${SERVER_IP}/api/v1/myreviews/?userId=${this.userId}`, this.options)
        .then(response => {
          this.$store.dispatch('setUserMovie', response.data)
          console.log(response.data)
        })
        .catch(error => {
          console.error(error)
        })
    },
    dateToStr(format) {
      const year = format.getFullYear()
      let month = format.getMonth() + 1
      if(month<10) month = '0' + month
      let day = format.getDate();
      if(day<10) day = '0' + day
      return year + "-" + month + "-" + day
    },
    openDiary(selectedDate) {
      this.$store.dispatch('clearDiary')
      const SERVER_IP = process.env.VUE_APP_SERVER_IP
      
      axios.get(`${SERVER_IP}/diaries/diaries/?userId=${this.userId}&datetime=${this.dateToStr(selectedDate)}`, this.options)
        .then(response => {
          if(response.data === false) {
            router.push()
          }
        })
        .catch(error => {
          console.error(error)
        })
    },
  },
  mounted() {
    console.log(this.userId)
    this.getUserInfo()
    this.getUserMovie()
  }
}
</script>

<style>

</style>