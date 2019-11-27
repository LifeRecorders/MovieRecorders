<template>
  <div>

    <div class="text-center">
      <v-date-picker
        mode='single'
        tint-color='#ff8080'
        v-on:input='selectDay'
        v-model='selectedDate'
        v-bind:theme-styles='themeStyles'
        is-inline>
      </v-date-picker>
    </div>
    
  </div>
</template>

<script>
import Vue from 'vue'
import VCalendar from 'v-calendar'
import 'v-calendar/lib/v-calendar.min.css'

Vue.use(VCalendar, {
  firstDayOfweek: 2
})

export default {
  name: 'app',
  data () {
    return {
      selectedDate: null,
      themeStyles: {
        wrapper: {
          border: '1',
          backgroundColor: '#ffffff'
        },
        header: {
          color: '#fafafa',
          backgroundColor: '#ff8080',
          borderColor: '#404c59',
          borderWidth: '1px 1px 0 1px',
        },
        headerVerticalDivider: {
          borderLeft: '1px solid #404c59',
        },
        weekdays: {
          color: '#ffffff',
          backgroundColor: '#ff8080',
          borderColor: '#ff0098',
          borderWidth: '0 1px',
          padding: '5px 0 10px 0',
        },
        weekdaysVerticalDivider: {
          borderLeft: '1px solid #404c59',
        },
        weeks: {
          border: '1px solid #dadada',
        },
      },
    };
  },
  methods: {
    selectDay() {
      console.log('click!')
      console.log(this.selectedDate)
      this.$emit('openDiary', this.selectedDate)
      this.selectedDate = null
    },
  }
}
</script>

<style>

</style>