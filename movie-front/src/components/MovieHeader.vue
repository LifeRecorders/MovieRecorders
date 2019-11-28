<template>
  <div id="movie_header">
    <b-navbar toggleable="lg">
      <b-navbar-brand>
        <router-link to="/" id="router_home" class="text-dark">Home</router-link>
      </b-navbar-brand>
      <!-- <b-navbar-brand>
        <img src="@/assets/images/logo_small.png" v-on:click="homeRouter" v-bind="mainProps"/>
      </b-navbar-brand> -->

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav v-if="isLoggedIn" class="ml-auto">
          <b-nav-item-dropdown class="text-dark" right>
            <template v-slot:button-content>
              <em>User</em>
            </template> 
            
            <b-dropdown-item><router-link to="/mypage/" id="router_mypage">My Page</router-link></b-dropdown-item>
            <b-dropdown-item v-on:click.prevent="logout" href="/logout">로그아웃</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
        <b-navbar-nav v-else class="ml-auto">
          <LoginForm />
          <SignUpForm />
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
import router from "@/router";
import SignUpForm from "@/components/SignUpForm";
import LoginForm from "@/components/LoginForm";

export default {
  name: "movie_header",
  data() {
    return {
      mainProps: {
        blank: true,
        blankColor:'#777',
        width: 75,
        height: 75,
        class: 'm1'
      }
    }
    
  },
  components: {
    LoginForm,
    SignUpForm
  },
  computed: {
    isLoggedIn() {
      return this.$store.getters.isLoggedIn;
    }
  },
  methods: {
    homeRouter() {
      router.push('/');
    },
    logout() {
      this.$session.destroy();
      this.$store.dispatch("logout");
      router.push("/");
    }
  }
};
</script>

<style>
#router_home {
  display: inline-block;
}
</style>