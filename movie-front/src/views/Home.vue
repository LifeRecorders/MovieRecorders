<template>
  <div class="home">
    <header v-bind:style="{ backgroundImage: 'url(' + require('@/assets/images/maincolor.png') +')'}">
      <MovieHeader />
      <h1 class="title">MovieRecorders</h1>
      <p class="subtitle">We record your film life.</p>
      <div id="searchBarDiv" class="container col-6 mt-5">
        <SearchBar id="searchBar" v-on:searchInfo="searchInfo"/>
      </div>
    </header>
    <br/>
    <br/>
    <div class="container">
      <v-menu
        transition="slide-y-transition"
        bottom
      >
        <template v-slot:activator="{ on }">
          <v-btn
            class="purple mb-5"
            color="primary"
            dark
            v-on="on"
          >
            어떤 영화를 좋아하세요?
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            v-for="(genre, i) in this.genres"
            :key="i"
            v-on:click="getGenreMovies(genre)"
          >
            <v-list-item-title>{{ genre }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <h5 class="genre-type"> {{this.genre}} </h5>
      <!-- {{ this.genreMovies }} -->
      <b-card-group deck>
        <div v-for="(movie, idx) in this.genreMovies" v-bind:key="idx">
          <b-card
          border-variant="white"
          align="left"
          img-alt="Image"
          img-top
          tag="article"
          style="max-width: 12rem;"
          class="mb-2">
            <b-card-img rounded alt="Rounded image" class="mb-3" v-bind:src="movie.naver_big_poster_url" v-on:click="getDetail(idx)">
            </b-card-img>
            <b-card-title>
              <h5 class="mb-0">{{ movie.title }}</h5>
            </b-card-title>
            <b-card-text>
              <p>{{ getYear(movie.open_date) }} · {{ movie.nation }}</p>
            </b-card-text>
          </b-card>
        </div>
      </b-card-group>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import MovieHeader from '@/components/MovieHeader'
import SearchBar from '@/components/SearchBar'
import router from '@/router'
import axios from 'axios'


export default {
  name: 'Home',
  computed: {
    ...mapState(['bestMovies'])
  },
  components: {
    MovieHeader,
    SearchBar,
  },
  data() {
    return {
      genre: '인기 영화',
      genres: ['인기 영화', '애니메이션', '범죄', '드라마', '액션', '어드벤처', 'SF', '멜로/로맨스',
      '스릴러', '판타지', '코미디', '가족', '공포(호러)', '다큐멘터리', '전쟁', '사극', '미스터리'],
      genreMovies: []
    }
  },
  methods: {
    async searchInfo(keyword) {
      await this.$store.dispatch('searchInfo', keyword)
      router.push(`/search/${keyword}`)
    },
    setBestMovies() {
      this.genreMovies = this.bestMovies
    },
    getGenreMovies(genre) {
      if ("인기 영화" === genre) {
        this.genre = genre
        this.setBestMovies()
        return
      }
      const SERVER_IP = process.env.VUE_APP_SERVER_IP
      console.log(genre)

      axios.get(`${SERVER_IP}/api/v1/movies_with_genre/?genretype=${genre}`)
        .then(response => {
          console.log(response)
          this.genreMovies = response.data
          this.genre = genre
        })
        .catch(error => {
          console.error(error)
        })
    },
    getYear(date) {
      const year = date.substring(0, 4)
      return year
    },
    getDetail(idx) {
      const detailData = this.genreMovies[idx]
      console.log(detailData)
      const keyword = this.genreMovies[idx].title
      this.$store.dispatch('showDetail', detailData)
      router.push(`/detail/${keyword}`)
    },    
  },
  created: function() {
    const SERVER_IP = process.env.VUE_APP_SERVER_IP

      axios.get(`${SERVER_IP}/api/v1/bestmovies/`)
        .then(response => {
          console.log(response.data)
          this.$store.dispatch('setBestMovies', response.data)
          this.genreMovies = response.data
        })
        .catch(error => {
          console.error(error)
        })
    console.log(this.genreMovies)
  }
}
</script>

<style>
.home > header {
  background-size: cover;
  height: 20rem;
  width: 100%;
  background-position-x: center;
}
.home #searchBarDiv {
  position: relative;
  top: 1.5rem;
}
.title {
  position: relative;
  top: 3rem;
  color: white;
  text-align: center;
}
.subtitle {
  position: relative;
  top: 3rem;
  color: white;
  text-align: center;
}

.genre-type {
  text-align: center;
}
</style>