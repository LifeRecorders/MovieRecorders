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
      <b-card align="right" border-variant="secondary" style="max-width: 100rem;">
        <b-button v-b-modal.modal-review size="md" variant="outline-secondary">감상평 남기기</b-button>

        <b-modal
        id="modal-review"
        ref="modal"
        v-bind:title="this.detail.title"
        v-on:show="resetModal"
        v-on:hidden="resetModal"
        v-on:ok="reviewOk">
          <b-form-group v-bind:state="reviewState" label="Review" label-for="review-input">
            <b-form-input id="review-input" v-model="review" v-bind:state="reviewState" required>
            </b-form-input>
          </b-form-group>
        </b-modal>
      </b-card>
    </div>
    <div class="container mt-3 text-left">
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
          <h6 v-html="replaceAll(this.detail.description)"></h6>
          <br/>
          <hr/>
          <br/>
        </b-text>
        <b-text>
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
        </b-text>
        <b-text>
          <h4>감상평</h4>
          <br>
        </b-text>
        <div>
          <b-card no-body>
            <b-tabs card>
              <b-tab title="전체" active>
                <b-card-text>Tab contents 1</b-card-text>
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
// import axios from'axios'
import { mapState } from 'vuex'

export default {
  name: "Detail",
  data() {
    return {
      review: '',
      reviewState: null,
    }
  },
  computed: {
    ...mapState(['detail'])
  },
  methods: {
    getYear(date) {
      const year = date.substring(0, 4)
      return year
    },
    replaceAll(str) {
      const result = str.replace(/\r/, "\n")
      return result
    },
    getReview() {
      // const SERVER_IP = process.env.VUE_APP_SERVER_IP
    }
  }
}
</script>

<style>

</style>