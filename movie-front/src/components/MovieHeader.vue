<template>
  <div id="movie_header">
    <b-navbar toggleable="lg" type="dark" variant="white">
      <b-navbar-brand>
        <router-link to="/" id="router_home" class="text-dark">Home</router-link>
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <!-- Right aligned nav items -->
        <b-navbar-nav v-if="isLoggedIn">
          <!-- <a v-on:click.prevent="logout" href="/logout">로그아웃</a> -->
          <b-nav-item-dropdown right>
            <!-- Using 'button-content' slot -->
            <template v-slot:button-content>
              <em>User</em>
            </template>
            <b-dropdown-item href="#">Profile</b-dropdown-item>
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