<template>
  <div>
    <div v-if="this.info.movies.length > 0">
      <hr/>
      <p class="text-left ml-3">영화</p>
      <div v-for="(movie, idx) in this.info.movies" v-bind:key="idx">
        
      </div>
    </div>
    <div v-if="this.info.artists.length > 0">
      <hr/>
      <p class="text-left ml-3">배우/제작</p>
      <div v-for="(artist, idx) in this.info.artists" v-bind:key="idx">
        
      </div>
    </div>
    <div v-if="this.info.users.length > 0">
      <hr/>
      <p class="text-left ml-3">사용자</p>
      <div v-for="(user, idx) in this.info.users" v-bind:key="idx">
        
      </div>
    </div>
    
  </div>
</template>

<script>
import { mapState } from "vuex";
import axios from "axios";
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
    getMovieDetail(movie) {
      const SERVER_IP = process.env.VUE_APP_SERVER_IP;
      axios
        .get(`${SERVER_IP}/api/v1/movies/${movie.id}/`)
        .then(response => {
          this.detail = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
    getDirectorDetail(director) {
      const SERVER_IP = process.env.VUE_APP_SERVER_IP;
      axios
        .get(`${SERVER_IP}/api/v1/directors/${director.id}/`)
        .then(response => {
          this.detail = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
    getActorDetail(actor) {
      const SERVER_IP = process.env.VUE_APP_SERVER_IP;
      axios
        .get(`${SERVER_IP}/api/v1/actors/${actor.id}/`)
        .then(response => {
          this.detail = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
    getUserDetail(user) {
      const SERVER_IP = process.env.VUE_APP_SERVER_IP;
      axios
        .get(`${SERVER_IP}/api/v1/users/${user.id}/`)
        .then(response => {
          this.detail = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    }
  }
};
</script>

<style>
</style>