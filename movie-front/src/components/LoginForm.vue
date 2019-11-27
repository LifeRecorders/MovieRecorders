<template>
  <div id="login-div">
    <b-button variant="white" v-b-modal.login-modal>로그인</b-button>

    <div v-if="loading" class="spinner-border" role="status">
      <span class="sr-only">loading...</span>
    </div>

    <b-modal id="login-modal" ref="modal" title="로그인" v-on:show="resetModal" v-on:ok="loginOk">
      <form ref="form" v-on:submit.stop.prevent="login">
        <b-form-group v-bind:state="usernameState" invalid-feedback="아이디를 입력해주세요.">
          <b-form-input id="username-input" v-model="credentials.username" v-bind:state="usernameState" placeholder="ID" required></b-form-input>
        </b-form-group>
        <b-form-group v-bind:state="passwordState" invalid-feedback="비밀번호를 입력해주세요.">
          <b-form-input type="password" id="password-input" v-model="credentials.password" v-bind:state="passwordState" placeholder="비밀번호" required></b-form-input>
        </b-form-group>
        <!-- <b-form-group>
          <b-button type="submit" size="md" variant="primary">로그인</b-button>
        </b-form-group> -->
      </form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios'
import router from '@/router'
export default {
  name: 'LoginForm',
  data() {
    return {
      credentials: {
        username: '',
        password: '',
      },
      usernameState: null,
      passwordState: null,
      loading: false,
      errors: [],
    }
  },
  methods: {
    resetModal() {
      this.credentials.username = ''
      this.usernameState = null
      this.credentials.password = ''
      this.passwordState = null
    },
    loginOk(byModalEvt) {
      byModalEvt.preventDefault()
      console.log(this.credentials)
      this.login()
    },
    login() {
      if(this.checkForm()) {
        this.loading = true
        const SERVER_IP = process.env.VUE_APP_SERVER_IP
        console.log(this.credentials)
        axios.post(SERVER_IP + '/api-token-auth/', this.credentials)
          .then(response => {
            console.log(response)
            this.$session.start()
            this.$session.set('jwt', response.data.token)
            this.$store.dispatch('login', response.data.token)

            this.loading = false

            router.push('/')
          })
          .catch(error => {
            console.log(error)
            this.loading = false
          })
      }
      this.$nextTick(() => {
        this.$refs.modal.hide()
      })
    },
    checkForm() {
      this.errors = []
      if(!this.credentials.username) {
        this.errors.push('이메일을 입력하세요')
      }
      if(this.credentials.password.length < 2) {
        this.errors.push('비밀번호는 8글자 이상 입력해주세요.')
      }
      if(this.errors.length === 0) {
        return true
      }
    },
  },
}
</script>

<style>
#login-div {
  display: inline-block;
}

.loginModalTitle {
  text-align: center;
}
</style>