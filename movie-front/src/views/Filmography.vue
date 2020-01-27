<template>
  <div id="filmography" v-bind:style="{ backgroundImage: 'url(' + require('@/assets/images/backgroundcolor.png') +')'}">
    <header>
      <MovieHeader />
      <div id="searchBarDiv" class="container col-6 mt-5">
        <SearchBar id="searchBar" v-on:searchInfo="searchInfo"/>
      </div>
    </header>
    <!-- {{ this.filmography }} -->
    <div class="container">
      <b-card>
        <!-- {{ this.info.movies }} -->
        <b-img v-bind:src="this.filmography.img_url" rounded="circle" alt="artist-img" id="artist-img" class="mb-2" center></b-img>
        <h6 style="text-align:center">{{ filmography.name }}</h6>
        <hr/>
        <b-card-group deck>
          <div v-for="(movie, idx) in this.filmography.movies" v-bind:key="idx">
            <b-card
            border-variant="white"
            align="left"
            img-alt="Image"
            img-top
            tag="article"
            style="max-width: 10rem;"
            class="mb-2">
            <b-card-img rounded alt="Rounded image" class="mb-3" v-bind:src="movie.naver_big_poster_url" v-on:click="getDetail(idx)">
            </b-card-img>
            <b-card-title>
                <h6>{{ movie.title }}</h6>
            </b-card-title>
            <b-card-text style="font-size:small;">
                <p>{{ getYear(movie.open_date) }} · {{ movie.nation }}</p>
            </b-card-text>
            </b-card>
          </div>
        </b-card-group>
      </b-card>
      
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import axios from 'axios'
import router from '@/router'
import MovieHeader from '@/components/MovieHeader'
import SearchBar from '@/components/SearchBar'

export default {
  name: "Filmography",
  data() {
    return {
      detail: ""
    };
  },
  components: {
    MovieHeader,
    SearchBar
  },
  computed: {
    ...mapState(["filmography"])
  },
  methods: {
    searchInfo(keyword) {
      this.$store.dispatch('searchInfo', keyword)
    },
    getYear(date) {
      const year = date.substring(0, 4)
      return year
    },
    getDetail(idx) {
      this.$store.dispatch('clearDetail')
      let pk = this.filmography.movies[idx].pk
      let keyword = this.filmography.movies[idx].title
      const SERVER_IP = process.env.VUE_APP_SERVER_IP

      axios.get(`${SERVER_IP}/api/v1/personsmovie/?q=${pk}`)
        .then(response => {
          const info = response.data
          console.log(info.movie)
          this.$store.dispatch('showDetail', info.movie[0])
          router.push(`/detail/${keyword}`)
        })
        .catch(error => {
          console.error(error)
        })
      
    },
  }
};
</script>

<style>
#filmography > header {
  background-size: cover;
  height: 3rem;
  width: 100%;
  background-position-x: center;
}
#filmography #searchBarDiv {
  position: relative;
  top: -5.2rem;
}
#artist-img { 
  width: 4rem; 
  height: 4rem; 
  object-fit: cover;
  text-align: center;
}
</style>