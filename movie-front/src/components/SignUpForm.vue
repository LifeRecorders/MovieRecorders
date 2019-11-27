<template>
  <div id="signup-div">
    <b-button variant="primary" v-b-modal.signupModal>회원가입</b-button>

    <div v-if="loading" class="spinner-border" role="status">
      <span class="sr-only">loading...</span>
    </div>

    <b-modal id="signupModal" ref="modal" title="회원가입" title-class="signupModalTitle" v-on:show="resetModal" v-on:ok="signUpOk">
      <form ref="form" v-on:submit.stop.prevent="signUp">
        <b-form-group v-bind:state="usernameState" invalid-feedback="ID를 입력해주세요.">
          <b-form-input id="username-input" v-model="credentials.username" v-bind:state="usernameState" placeholder="ID" required></b-form-input>
        </b-form-group>
        <b-form-group v-bind:state="passwordState" invalid-feedback="비밀번호를 입력해주세요.">
          <b-form-input type="password" id="password-input" v-model="credentials.password" v-bind:state="passwordState" placeholder="비밀번호" required></b-form-input>
        </b-form-group>
        <b-form-group v-bind:state="emailState" invalid-feedback="이메일을 입력해주세요.">
          <b-form-input type="text" id="email-input" v-model="credentials.email" v-bind:state="emailState" placeholder="email" required></b-form-input>
        </b-form-group>
      </form>
      <!-- <template v-slot:modal-footer="{ close }">
        <b-button type="submit" size="md" variant="primary" @click="signUp()">
          회원가입
        </b-button>
    </template>  -->
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios'
import router from '@/router'

export default {
  name: 'SignUpForm',
  data() {
    return {
      credentials: {
        username: '',
        password: '',
        email: '',
      },
      usernameState: null,
      passwordState: null,
      emailState: null,
      loading: false,
      erorrs: [],
    }
  },
  methods: {
    resetModal() {
      this.credentials.username = ''
      this.usernameState = null
      this.credentials.password = ''
      this.passwordState = null
      this.credentials.email = ''
      this.emailState = null
    },
    signUpOk(byModalEvt) {
      byModalEvt.preventDefault()
      console.log(this.credentials)
      this.signUp()
    },
    signUp() {
      if(this.checkForm()) {
        this.loading = true
        const SERVER_IP = process.env.VUE_APP_SERVER_IP
        console.log(this.credentials)

        axios.post(SERVER_IP + '/accounts/register/', this.credentials)
          .then(response => {
            console.log(response)
            router.push('/')
            this.loading = false
            // if(response.status === 200) {
            //   this.loading = false
              // router.push('/')
            // }
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
        this.errors.push('ID를 입력하세요.')
      }
      if(this.credentials.password.length < 8) {
        this.errors.push('비밀번호는 8글자 이상 입력해주세요.')
      }
      if(!this.credentials.email) {
        this.errors.push('이메일을 입력해주세요.')
      }
      if(this.errors.length === 0) {
        return true
      }
    }
  }

}
</script>

<style>
#signup-div {
  display: inline-block;
}
</style>