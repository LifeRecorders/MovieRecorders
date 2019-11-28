<template>
  <div>
    <div class="bgBlur" v-bind:style="{ backgroundImage: 'url(' + this.bgImageUrl + ')' }"></div>
    <!-- {{ this.detail }} -->
    <div id="detail">
      <header>
      <MovieHeader />
      <div id="searchBarDiv" class="container col-6 mt-5">
        <SearchBar id="searchBar" v-on:searchInfo="searchInfo"/>
      </div>
      </header>
      <b-container>
        <b-card style="padding-bottom: 0;" class="cdBackground mt-5 mb-5" v-bind:style="{ backgroundImage: 'url(' + this.bgImageUrl + ')' }">
          <b-row class="mb-4">
            <b-col md="8">
            <div style="visibility:hidden; width:15rem; height:15rem;"></div>
            </b-col>
            <b-col>
            </b-col>
            
          </b-row>

          <b-row class="text-left mt-2 mb-0">
            <b-col md="4">
              <h2>{{ this.detail.title }}</h2>
              <h6 style="font-size:small;">{{ getYear(this.detail.open_date) }} · {{ this.detail.nation }}</h6>
              <h6 style="font-size:small;" class="mt-2">{{ this.detail.watch_grade }}</h6>
              <h6 class="rating mr-3">평점 ★{{ this.detail.rating }}</h6>
              <b-button size="sm" class="mr-3" id="likeButton" v-on:click="want">보고 싶어요</b-button>
              <b-button v-b-modal.modal-diary size="sm" variant="light">내 다이어리 쓰기</b-button>
                <b-modal
                id="modal-diary"
                ref="modal"
                v-bind:title="this.detail.title"
                v-on:show="resetDiaryModal"
                v-on:hidden="resetDiaryModal"
                v-on:ok="diaryOk">
                  <b-form-group v-bind:state="diaryTitleState">
                    <DiaryCalendar v-on:openDiary="openDiary" />
                    <br/>
                    <div class="text-center" v-text="this.watched_at"></div>
                    <br/>
                    <b-form-input id="title-input" v-model="diaryTitle" v-bind:state="diaryTitleState" placeholder="Title" required>
                    </b-form-input>
                  </b-form-group>
                  <b-form-group v-bind:state="diaryContentState">
                    <b-form-input id="content-input" v-model="diaryContent" v-bind:state="diaryContentState" placeholder="이 영화를 본 날은 어땠나요?" required>
                    </b-form-input>
                  </b-form-group>
                </b-modal>
              <hr style="border: 0.5px solid white"/>
              
            </b-col>
          </b-row>
          <br/>
          
        </b-card>
        <b-card class="text-left">
          <br/>
          <b-row>
            <b-col md="10">
              <div class="mb-0">{{ this.detail.description }}</div>
            </b-col>
          </b-row>
          <br/>
          <hr/>
          <h4>제작/출연</h4>
          <br/>  
          <b-row>
            <br/>
            <div style="font-size:small;" v-for="(director, idx) in this.detail.directors" v-bind:key="idx">
              <b-col style="padding-left: 1rem; padding-right: 0;" class="text-center mr-3">
                <b-img v-bind:src="director.img_url" rounded="circle" alt="director-img" id="director-img" class="mb-2"></b-img>
                <br/>
                {{ director.name }}
              </b-col>
            </div>
          </b-row>
          <br>
          <b-row>
            <br/>
            <div style="font-size:small;" v-for="(actor, idx) in this.detail.actors" v-bind:key="idx">
              <b-col style="padding-left: 1rem; padding-right: 0;" class="text-center mr-3">
                <b-img v-bind:src="actor.img_url" rounded="circle" alt="actor-img" id="actor-img" class="mb-2"></b-img>
                <br/>
                {{ actor.name }}
              </b-col>
            </div>
          </b-row>
          <br/>
          <hr/>
          <br/>

          <b-row>
            <b-col>
              <span style="font-size:x-large; position: relative; top: -1.2rem;">감상평</span>
              <div id="review-button" v-if="isLoggedIn" style="position: relative; top: -1.55rem; right: -1rem;" class="container text-left pl-0">
                <b-button v-b-modal.modal-review size="sm" variant="light" class="ml-auto">감상평 남기기</b-button>
                <b-modal
                id="modal-review"
                ref="modal"
                v-bind:title="this.detail.title"
                v-on:show="resetModal"
                v-on:hidden="resetModal"
                v-on:ok="reviewOk">
                  <star-rating v-bind:increment="0.5" v-bind:star-size="30" v-on:rating-selected="setScore"></star-rating>
                  <br/>
                  <b-form-group v-bind:state="reviewState">
                    <b-form-input id="review-input" v-model="review" v-bind:state="reviewState" placeholder="이 작품은 어떠셨나요?" required>
                    </b-form-input>
                  </b-form-group>
                </b-modal>
              </div>
              <br/>
              <b-row>
                <div v-for="(review, idx) in this.reviews.slice(0, 3)" v-bind:key="idx">
                  <b-card class="mx-2" body-class="px-0 py-3">
                    <b-col>
                      {{ review.user.username }}
                      ★{{ review.score }}
                      <hr/>
                      {{ review.content }}<br/>
                    </b-col>
                  </b-card>
                </div>
              </b-row>
            </b-col>
          </b-row>
          <br/>
          <hr/>
          <h4>갤러리</h4>
          <div>
            <b-carousel
              id="carousel-fade"
              class="mt-5 mb-5"
              style="text-shadow: 0px 0px 2px #000"
              fade
              controls
              indicators
              img-width="500"
              img-height="200"
            >
              <div v-for="(scene, idx) in this.detail.scenes.slice(1, this.detail.scenes.length)" v-bind:key="idx">
                <b-carousel-slide
                v-bind:img-src="scene.scene">
                </b-carousel-slide>
              </div>
            </b-carousel>
          </div>
        </b-card>
      </b-container>
    </div>
  </div>
</template>

<script>
import axios from'axios'
import { mapState, mapGetters } from 'vuex'
import StarRating from 'vue-star-rating'
import DiaryCalendar from '@/components/DiaryCalendar'
import MovieHeader from '@/components/MovieHeader'
import SearchBar from '@/components/SearchBar'

export default {
  name: "Detail",
  data() {
    return {
      review: '',
      reviewState: null,
      reviews: [],
      score: null,
      diaryTitle: '',
      diaryContent: '',
      watched_at: '',
      diaryFile: '',
      diaryTitleState: null,
      diaryContentState: null,
      bgImageUrl: '',
      mainReview: [],
    }
  },
  components: {
    StarRating,
    DiaryCalendar,
    MovieHeader,
    SearchBar
  },
  computed: {
    ...mapGetters([
      'options',
      'userId'
    ]),
    ...mapState(['detail']),
    isLoggedIn() {
      return this.$store.getters.isLoggedIn;
    },
  },
  methods: {
    searchInfo(keyword) {
      this.$store.dispatch('searchInfo', keyword)
    },
    resetModal () {
      this.review = ''
      this.reviewState = null
    },
    resetDiaryModal() {
      this.diaryTitle = ''
      this.diaryTitleState = null
      this.diaryContent = ''
      this.diaryContentState = null
      this.watched_at = ''
    },
    reviewOk(byModalEvt) {
      byModalEvt.preventDefault()
      this.createReview()
    },
    getYear(date) {
      const year = date.substring(0, 4)
      return year
    },
    replaceAll(str) {
      const result = str.replace(/\r/, "\n")
      return result
    },
    getReview(movieId) {
      const SERVER_IP = process.env.VUE_APP_SERVER_IP

      axios.get(`${SERVER_IP}/api/v1/reviews/?movieId=${movieId}`, this.options)
        .then(response => {
          this.reviews = response.data
        })
        .catch(error => {
          console.error(error)
        })
    },
    createReview() {
      const SERVER_IP = process.env.VUE_APP_SERVER_IP
      const data = {
        movie: this.detail.pk,
        user: this.userId,
        content: this.review,   
        score: this.score,     
      }
      console.log(data)
      axios.post(`${SERVER_IP}/api/v1/reviews_create_update_delete/?movieId=${this.detail.pk}`, data, this.options)
        .then(response => {
          console.log(response)
        })
        .catch(error => {
          console.error(error)
        })
      this.$nextTick(() => {
        this.$refs.modal.hide()
      })
    },
    setScore(score) {
      this.score = score
    },
    dateToStr(format) {
      const year = format.getFullYear()
      let month = format.getMonth() + 1
      if(month<10) month = '0' + month
      let day = format.getDate();
      if(day<10) day = '0' + day
      return year + "-" + month + "-" + day
    },
    openDiary(selectedDate) {
      this.watched_at = this.dateToStr(selectedDate)
      return this.watched_at
    },
    diaryOk(byModalEvt) {
      byModalEvt.preventDefault()
      this.writeDiary()
    },
    writeDiary() {
      const SERVER_IP = process.env.VUE_APP_SERVER_IP
      const data = {
        title: this.diaryTitle,
        content: this.diaryContent,
        watched_at: this.watched_at,
        movies: this.detail.pk,
        user: this.userId
      }

      axios.post(`${SERVER_IP}/diaries/diaries/diaries_create_update_delete/?userId=${data.user}&datetime=${data.watched_at}`, data, this.options)
        .then(response => {
          console.log(response)
        })
        .catch(error => {
          console.error(error)
        })
        this.$nextTick(() => {
        this.$refs.modal.hide()
      })
    },
    setBgImage() {
      if(this.detail.scenes.length > 0) {
        if(this.detail.scenes.length > 1) {
          this.bgImageUrl = this.detail.scenes[1]['scene']
        }
        else {
          this.bgImageUrl = this.detail.scenes[0]['scene']
        }
      }
    },
    want() {
      const SERVER_IP = process.env.VUE_APP_SERVER_IP

      axios.get(`${SERVER_IP}/api/v1/want/${this.detail.pk}/${this.userId}/`)
        .then(response => {
          console.log(response.data)
        })
        .catch(error => {
          console.error(error)
        })
    }

  },
  mounted() {
    this.getReview(this.detail.pk)
    this.setBgImage()
  },
}
</script>

<style>
/* html { overflow: hidden; } */
/* .bgBlur { overflow: auto; } */
.bgBlur {
  position: fixed; 
  top: 0; 
  left: 0; 
  right: 0; 
  bottom: 0; 
  background-size: cover; 
  -webkit-filter: blur(5px); 
  -moz-filter: blur(5px); 
  -o-filter: blur(5px); 
  -ms-filter: blur(5px); 
  filter: blur(15px); 
  transform: scale(1.02); 
  z-index: -1; 
  content: "";
  width:100%;
  height:100%;

}
#detail > header {
  background-color: white;
  background-size: cover;
  height: 3rem;
  width: 100%;
  background-position-x: center;
}
#detail #searchBarDiv {
  position: relative;
  top: -6.2rem;
}
.cdBackground {
  background-position: center;
  background-size: cover; 
  text-align: left;
  color: aliceblue;
}
.rating {
  display: inline;
}
#review-button {
  display: inline;
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
b-carousel-slide {
  overflow: hidden;
}
</style>