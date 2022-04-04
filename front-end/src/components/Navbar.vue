<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light" style="margin-bottom: 20px;">
    <div class="container">
      <router-link class="navbar-brand" to="/">
        <img alt="" class="d-inline-block align-top" height="30"
             src="https://getbootstrap.com/docs/4.1/assets/brand/bootstrap-solid.svg" width="30">
        MadBlog
      </router-link>
      <button aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation"
              class="navbar-toggler" data-target="#navbarSupportedContent" data-toggle="collapse" type="button">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div id="navbarSupportedContent" class="collapse navbar-collapse">
        <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
          <li class="nav-item active">
            <router-link class="nav-link" to="/">Home <span class="sr-only">(current)</span></router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link disabled" href="#">Explore</a>
          </li>
        </ul>

        <form v-if="sharedState.is_authenticated" class="form-inline navbar-left mr-auto">
          <input class="form-control mr-sm-2" placeholder="Search" type="search">
          <!-- 暂时先禁止提交，后续实现搜索再改回 type="submit" -->
          <button class="btn btn-outline-success my-2 my-sm-0" type="button">Search</button>
        </form>

        <ul v-if="sharedState.is_authenticated" class="nav navbar-nav navbar-right">
          <li class="nav-item">
            <a class="nav-link disabled" href="#">Messages</a>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/profile">Profile</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" v-on:click="handlerLogout">Logout</a>
          </li>
        </ul>
        <ul v-else class="nav navbar-nav navbar-right">
          <li class="nav-item">
            <router-link class="nav-link" to="/login">Login</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import store from '../store.js'

export default {
  name: 'Navbar',  //this is the name of the component
  data() {
    return {
      sharedState: store.state
    }
  },
  methods: {
    handlerLogout(e) {
      store.logoutAction()
      this.$router.push('/login')
    }
  }
}
</script>
