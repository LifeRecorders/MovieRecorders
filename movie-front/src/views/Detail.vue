<template>
  <div class="container">
    {{ this.detail }}
    <!-- 상단 이미지 + 정보 -->
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
      <b-card-sub-title>
        {{ getYear(this.detail.open_date) }} · {{ this.detail.nation }}
        <hr/>
      </b-card-sub-title>
      <b-card-text>
        <p>평점 {{ this.detail.rating }}</p>
      </b-card-text>
    </b-card>
    
    <!-- 감상평 남기기 -->
    <div v-if="isLoggedIn" class="container mt-5 text-left">
      <b-card align="right" border-variant="secondary" style="max-width: 100rem;">
        <b-button v-b-modal.modal-review size="md" variant="outline-secondary">감상평 남기기</b-button>

        <b-modal
        id="modal-review"
        ref="modal"
        v-bind:title="this.detail.title"
        v-on:show="resetModal"
        v-on:hidden="resetModal"
        v-on:ok="reviewOk">
          <star-rating></star-rating>
          <b-form-group v-bind:state="reviewState">
            <b-form-input id="review-input" v-model="review" v-bind:state="reviewState" placeholder="이 작품은 어떠셨나요?" required>
            </b-form-input>
          </b-form-group>
        </b-modal>
      </b-card>
    </div>

    <!-- 영화 상세 정보 -->
    <div class="container mt-3 text-left">
      <b-card
      border-variant="secondary"
      aligh="left"
      img-alt="Image"
      img-left
      style="max-width: 100rem;">
        <b-card-text>
          <h4>기본 정보</h4>
          <br/>
          <h6>{{ this.detail.title }}</h6>
          <h6>{{ getYear(this.detail.open_date) }} · {{ this.detail.nation }}</h6>
          <h6>{{ this.detail.watch_grade }}</h6>
          <br/>
          <h6 v-html="replaceAll(this.detail.description)"></h6>
          <br/>
          <hr/>
          <br/>
        </b-card-text>

        <b-card-text>
          <h4>출연/제작</h4>
          <br/>
          <dir v-for="(director, idx) in this.detail.directors" v-bind:key="idx">
            <div>
              <b-img width="100rem" height="100rem" left v-bind:src="director.img_url" rounded="circle"></b-img>
              {{ director.name }}
              <br/>
              제작
            </div>
          </dir>
          <br/>
          <hr/>
          <br/>
        </b-card-text>

        <b-card-text>
          <h4>감상평</h4>
          <br>
        </b-card-text>
        <div>
          <b-card no-body>
            <b-tabs card>
              <b-tab title="전체" active>
                <b-card-text>{{ this.reviews }}</b-card-text>
              </b-tab>
              <b-tab title="친구">
                <b-card-text>Tab contents 2</b-card-text>
              </b-tab>
            </b-tabs>
          </b-card>
        </div>
      </b-card>
    </div>
  </div>
</template>

<script>
import axios from'axios'
import { mapState, mapGetters } from 'vuex'
import StarRating from 'vue-star-rating'

export default {
  name: "Detail",
  data() {
    return {
      review: '',
      reviewState: null,
      reviews: []
    }
  },
  components: {
    StarRating
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
    resetModal () {
      this.review = ''
      this.reviewState = null
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
    }
  },
  mounted() {
    this.getReview(this.detail.pk)
  },
}
</script>

<style>

</style>