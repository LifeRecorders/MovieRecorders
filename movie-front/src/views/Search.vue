<template>
  <div id="search" v-bind:style="{ backgroundImage: 'url(' + require('@/assets/images/backgroundcolor.png') +')'}">
    <header>
      <MovieHeader />
      <div id="searchBarDiv" class="container col-6 mt-5">
        <SearchBar id="searchBar" v-on:searchInfo="searchInfo"/>
      </div>
    </header>
    <div class="container">
      <b-card>
        <div v-if="this.info.movies.length">
        <!-- {{ this.info.movies }} -->
        <hr/>
        <h3 class="text-left ml-1">영화</h3>
        <br/>
        <b-card-group deck>
            <div v-for="(movie, idx) in this.info.movies" v-bind:key="idx">
              <b-card
              border-variant="white"
              align="left"
              img-alt="Image"
              img-top
              tag="article"
              style="max-width: 10rem;"
              class="mb-2">
                <b-card-img rounded alt="Rounded image" class="mb-3" v-bind:src="movie.naver_big_poster_url" v-on:click="getDetail('movie', idx)">
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


        </div>
        <div v-if="this.info.directors.length">
          <hr/>
          <h3 class="text-left ml-1">제작</h3>
          <br/>
          <b-row>
            <div v-for="(director, idx) in this.info.directors" v-bind:key="idx">
              <b-col v-on:click="getFilmographyDirector(director.pk)" style="padding-left: 1rem; padding-right: 0;" class="text-left mr-3">
                <b-img v-bind:src="director.img_url" rounded="circle" alt="director-img" id="director-img" class="mb-2 text-center"></b-img>
                <br/>
                {{ director.name }}
              </b-col>
            </div>
          </b-row>
        </div>

        <div v-if="this.info.actors.length">
          <hr/>
          <h3 class="text-left ml-1">출연</h3>
          <br>
          <b-row>
            <div v-for="(actor, idx) in this.info.actors" v-bind:key="idx">
              <b-col v-on:click="getFilmographyActor(actor.pk)" style="padding-left: 1rem; padding-right: 0;" class="text-left mr-3">
                <b-img v-bind:src="actor.img_url" rounded="circle" alt="actor-img" id="actor-img" class="mb-2 text-center"></b-img>
                <br/>
                {{ actor.name }}
              </b-col>
            </div>
          </b-row>
        </div>

        <div v-if="this.info.users.length">
          <hr/>
          <p class="text-left ml-3">사용자</p>
          <div v-for="(user, idx) in this.info.users" v-bind:key="idx">
            
          </div>
        </div>
      </b-card>
      
        
      
      
      
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
// import axios from 'axios'
import router from '@/router'
import MovieHeader from '@/components/MovieHeader'
import SearchBar from '@/components/SearchBar'

export default {
  name: "Search",
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
    ...mapState(["info"])
  },
  methods: {
    searchInfo(keyword) {
      this.$store.dispatch('searchInfo', keyword)
    },
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
      console.log(detailData)
      this.$store.dispatch('showDetail', detailData)
      router.push(`/detail/${keyword}`)
    },
    getFilmographyDirector(id) {
      this.$store.dispatch('clearFilmography')
      this.$store.dispatch('setFilmographyDir', id)
    },
    getFilmographyActor(id) {
      this.$store.dispatch('clearFilmography')
      this.$store.dispatch('setFilmographyActor', id)
    }
  }
};
</script>

<style>
#search > header {
  background-size: cover;
  height: 3rem;
  width: 100%;
  background-position-x: center;
}
#search #searchBarDiv {
  position: relative;
  top: -5.2rem;
}
#director-img { 
  width: 4rem; 
  height: 4rem; 
  object-fit: cover; 
}
#actor-img { 
  width: 4rem; 
  height: 4rem; 
  object-fit: cover; 
}
</style>