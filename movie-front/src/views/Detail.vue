<template>
  <div class="container">
    {{ this.detail }}
    <b-card
    border-variant="white"
    align="left"
    img-alt="Image"
    v-bind:img-src="this.detail.naver_big_poster_url"
    img-width="160rem"
    img-left
    tag="article"
    style="max-width: 100rem;">
      <!-- <b-card-img rounded alt="Rounded image" class="mb-3" v-bind:src="this.detail.naver_big_poster_url" v-on:click="getDetail('movie', idx)">
      </b-card-img> -->
      <b-card-title>
        <h3>{{ this.detail.title }}</h3>
      </b-card-title>
      <b-card-subtitle>
        {{ getYear(this.detail.open_date) }} · {{ this.detail.nation }}
        <hr/>
      </b-card-subtitle>
      <b-card-text>
        <p>평점 {{ this.detail.rating }}</p>
      </b-card-text>
    </b-card>
    <div class="container mt-5 text-left">
      <b-card
      border-variant="secondary"
      aligh="left"
      img-alt="Image"
      img-left
      style="max-width: 100rem;">
        <b-text>
          <h4>기본 정보</h4>
          <br/>
          <h6>{{ this.detail.title }}</h6>
          <h6>{{ getYear(this.detail.open_date) }} · {{ this.detail.nation }}</h6>
          <h6>{{ this.detail.watch_grade }}</h6>
          <br/>
          <h6>{{ replaceAll(this.detail.description}}</h6>

        </b-text>
      </b-card>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: "Detail",
  computed: {
    ...mapState(['detail'])
  },
  methods: {
    getYear(date) {
      const year = date.substring(0, 4)
      return year
    },
    replaceAll(str, searchStr, replaceStr) {
      return str.split(searchStr).join(replaceStr);
    }
  }
}
</script>

<style>

</style>