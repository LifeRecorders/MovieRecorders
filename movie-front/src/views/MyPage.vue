<template>
  <div>
    {{ this.user }}
    My Page
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import router from '@/router'
import axios from 'axios'


export default {
  name: "MyPage",
  data () {
    return {
      user: []
    }
  },
  computed: {
    ...mapGetters([
      'options',
      'userId'
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
      const SERVER_IP = process.env.VUE_APP_SERVER_IP

      axios.get(`${SERVER_IP}/accounts/users/${this.userId}`, this.options)
        .then(response => {
          this.user = response.data
        })
    }
  },
  mounted() {
    console.log(this.userId)
    this.getUserInfo()
  }
}
</script>

<style>

</style>