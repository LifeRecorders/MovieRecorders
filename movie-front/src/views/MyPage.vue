<template>
  <div class="myPage">
    <header v-bind:style="{ backgroundImage: 'url(' + require('@/assets/images/maincolor.png') +')'}">
      <MovieHeader />
      <div id="searchBarDiv" class="container col-6 mt-5">
        <SearchBar id="searchBar" v-on:searchInfo="searchInfo"/>
      </div>
      <div class="container text-left text-light">
        <h2>{{ this.user.username }}</h2>
        <br/>
        <router-link to="/user-movie-list/" id="router-movie-list">
          <h6 class="router-movie">내가 본 영화 {{ this.userMovieList.length }} </h6>
        </router-link>
        <h6>앞으로 볼 영화 </h6>
        <br/>
      </div>
    </header>
    <div class="mt-5">
      <DiaryCalendar v-b-modal.modal-diary-page v-on:openDiary="openDiary" />
      <b-modal
      id="modal-diary-page"
      ref="modal"
      v-bind:title="this.diary.title"
      v-on:show="resetDiaryModal"
      v-on:hidden="resetDiaryModal">
      </b-modal>
    </div>
  </div>
  
</template>

<script>
import { mapGetters, mapState } from 'vuex'
import router from '@/router'
import axios from 'axios'
import DiaryCalendar from '@/components/DiaryCalendar'
import MovieHeader from '@/components/MovieHeader'
import SearchBar from '@/components/SearchBar'


export default {
  name: "MyPage",
  // data () {
  //   return {
  //     user: [],
  //     userMovie: []
  //   }
  // },
  components: {
    DiaryCalendar,
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
      'userMovieList',
      'diary'
    ]),
    isLoggedIn() {
      return this.$store.getters.isLoggedIn;
    },
  },
  methods: {
    searchInfo(keyword) {
      this.$store.dispatch('searchInfo', keyword)
    },
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
      
      axios.get(`${SERVER_IP}/diaries/diaries/diaries_create_update_delete/?userId=${this.userId}&datetime=${this.dateToStr(selectedDate)}`, this.options)
        .then(response => {
          this.$store.dispatch('setDiary', response.data)
          console.log(response)
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
.myPage > header {
  background-size: cover;
  height: 20rem;
  width: 100%;
  background-position-x: center;
}
.myPage #searchBarDiv {
  position: relative;
  top: -5rem;
}
</style>