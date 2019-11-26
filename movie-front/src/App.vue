<template>
  <div id="app">
    <header>
      <MovieHeader/>
    </header>
               
    <router-view/>

  </div>
</template>

<script>
// import router from '@/router'
import MovieHeader from '@/components/MovieHeader'

export default {
  name: 'app',
  components: {
    MovieHeader
  },
  computed: {
    isLoggedIn() {
      return this.$store.getters.isLoggedIn
    }
  },
  mounted() {
    if(this.$session.has('jwt')) {
      const token = this.$session.get('jwt')
      this.$store.dispatch('login', token)
    }
  },
  // methods: {
  //   logout() {
  //     this.$session.destroy()
  //     this.$store.dispatch('logout')
  //     router.push('/')
  //   }
  // }
}

</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 10px;
}

header {
  background-size: cover;
  height: 4rem;
  width: 100%;
  background-position-x: center;
}
</style>
