<template>
  <div class="movie-input">
    <form class="input-group mb-3" v-on:submit.prevent="onSubmit">
      <input v-on:keyup.enter="onSubmit" v-model="keyword" type="text" class="form-control" placeholder="작품명, 배우, 감독, 사용자 검색">
    </form>
  </div>
  
</template>

<script>
export default {
  name: 'SearchBar',
  data() {
    return {
      keyword: ''
    }
  },
  methods: {
    onSubmit() {
      this.$store.dispatch('clearInfo')
      this.$emit('searchInfo', this.keyword)
      console.log(this.keyword)
      this.keyword = ''
    },
    noop() {

    }
  }
}
</script>

<style>

</style>