<template>
  <div>
    <div v-if="this.info.movies.length">
      {{ this.info.movies }}
      <hr/>
      <p class="text-left ml-3">영화</p>
      <div class="card-deck row">
        <div class="col-lg-3 col-md-4 col-sm-6 col-12 mt-3">
          <div v-for="(movie, idx) in this.info.movies" v-bind:key="idx">
            <b-card
            border-variant="white"
            align="left"
            img-alt="Image"
            img-top
            tag="article"
            style="max-width: 10rem;"
            class="mb-2">
              <b-card-img rounded alt="Rounded image" class="mb-3" v-bind:src="movie.naver_poster_url" v-on:click="getDetail('movie', idx)">
              </b-card-img>
              <b-card-title>
                {{ movie.title }}
              </b-card-title>
              <b-card-text>
                {{ getYear(movie.open_date) }} · {{ movie.nation }}
              </b-card-text>
            </b-card>
          </div>
        </div>
      </div>
      
    </div>
    <div v-if="this.info.directors.length">
      <hr/>
      <p class="text-left ml-3">배우/제작</p>
      <div v-for="(director, idx) in this.info.directors" v-bind:key="idx">
        {{ director }}
        
      </div>
    </div>
    <div v-if="this.info.users.length">
      <hr/>
      <p class="text-left ml-3">사용자</p>
      <div v-for="(user, idx) in this.info.users" v-bind:key="idx">
        
      </div>
    </div>
    
  </div>
</template>

<script>
import { mapState } from 'vuex'
// import axios from 'axios'
import router from '@/router'

export default {
  name: "Search",
  data() {
    return {
      detail: ""
    };
  },
  computed: {
    ...mapState(["info"])
  },
  methods: {
    getYear(date) {
      const year = date.substring(0, 4)
      return year
    },
    getDetail(type, idx) {
      let detailData
      let keyword
      if(type === 'movie') {
        detailData = this.info.movies[idx]
        keyword = this.info.movies[idx].title
      }
      else if(type === 'director') {
        detailData = this.info.directors[idx]
        keyword = this.info.directors[idx].name
      }
      else if(type === 'actor') {
        detailData = this.info.actors[idx]
        keyword = this.info.actors[idx].name
      }
      else if(type === 'user') {
        detailData = this.info.users[idx]
        keyword = this.info.users[idx].username
      }
      else {
        return false
      }
      this.$store.dispatch('showDetail', detailData)
      router.push(`/detail/${keyword}`)
    },
    // getDirectorDetail(director) {
    //   const SERVER_IP = process.env.VUE_APP_SERVER_IP;
    //   axios
    //     .get(`${SERVER_IP}/api/v1/directors/${director.id}/`)
    //     .then(response => {
    //       this.detail = response.data;
    //     })
    //     .catch(error => {
    //       console.error(error);
    //     });
    // },
    // getActorDetail(actor) {
    //   const SERVER_IP = process.env.VUE_APP_SERVER_IP;
    //   axios
    //     .get(`${SERVER_IP}/api/v1/actors/${actor.id}/`)
    //     .then(response => {
    //       this.detail = response.data;
    //     })
    //     .catch(error => {
    //       console.error(error);
    //     });
    // },
    // getUserDetail(user) {
    //   const SERVER_IP = process.env.VUE_APP_SERVER_IP;
    //   axios
    //     .get(`${SERVER_IP}/api/v1/users/${user.id}/`)
    //     .then(response => {
    //       this.detail = response.data;
    //     })
    //     .catch(error => {
    //       console.error(error);
    //     });
    // }
  }
};
</script>

<style>
</style>