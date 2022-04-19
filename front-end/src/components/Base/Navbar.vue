<template>
  <section>
    <div class="container">
      <nav class="navbar navbar-expand-lg navbar-light bg-light" style="margin-bottom: 20px;">
        <div class="navbar-brand">
          <router-link class="g-text-underline--none--hover" to="/">
            <img alt="" class="d-inline-block align-top" height="30" src="../../assets/logo.png" width="30">
            Design by
          </router-link>
          <a class="g-text-underline--none--hover" href="http://www.slhe.top">S_L_HE</a>
        </div>
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
              <router-link class="nav-link" to="/ping">Ping</router-link>
            </li>
            <li v-if="sharedState.is_authenticated && sharedState.user_perms.includes('admin')" class="nav-item">
              <router-link class="nav-link" to="/admin">Admin</router-link>
            </li>
          </ul>

          <form v-if="sharedState.is_authenticated" class="form-inline navbar-left mr-auto">
            <input class="form-control mr-sm-2" placeholder="Search" type="search">
            <!-- 暂时先禁止提交，后续实现搜索再改回 type="submit" -->
            <button class="btn btn-outline-success my-2 my-sm-0" type="button">Search</button>
          </form>

          <ul v-if="sharedState.is_authenticated" class="nav navbar-nav navbar-right">
            <li class="nav-item g-mr-20">
              <router-link class="nav-link" v-bind:to="{ path: '/notifications/comments' }"><i
                class="icon-education-033 u-line-icon-pro g-color-red g-font-size-16 g-pos-rel g-top-2 g-mr-3"></i>
                Notifications <span id="new_notifications_count"
                                    class="u-label g-font-size-11 g-bg-aqua g-rounded-20 g-px-10"
                                    style="visibility: hidden;">0</span></router-link>
            </li>
            <li class="nav-item dropdown">
              <a id="navbarDropdown" aria-expanded="false" aria-haspopup="true" class="nav-link dropdown-toggle"
                 data-toggle="dropdown" href="#" role="button">
                <img class="g-brd-around g-brd-gray-light-v3 g-pa-2 rounded-circle rounded mCS_img_loaded"
                     v-bind:src="sharedState.user_avatar"> {{ sharedState.user_name }}
              </a>
              <div aria-labelledby="navbarDropdown" class="dropdown-menu">
                <router-link class="dropdown-item" v-bind:to="{ path: `/user/${sharedState.user_id}` }"><i
                  class="icon-star g-pos-rel g-top-1 g-mr-5"></i> Your profile
                </router-link>
                <router-link class="dropdown-item" v-bind:to="{ name: 'PostsResource' }"><i
                  class="icon-share g-pos-rel g-top-1 g-mr-5"></i> Your resource
                </router-link>
                <router-link class="dropdown-item" v-bind:to="{ name: 'SettingProfile' }"><i
                  class="icon-settings g-pos-rel g-top-1 g-mr-5"></i> Settings
                </router-link>
                <div class="dropdown-divider"></div>
                <a class="dropdown-item" href="#" v-on:click="handlerLogout"><i
                  class="icon-logout g-pos-rel g-top-1 g-mr-5"></i> Sign out</a>
              </div>
            </li>
          </ul>
          <ul v-else class="nav navbar-nav navbar-right">
            <li class="nav-item">
              <router-link class="nav-link" to="/login"><i class="icon-login g-pos-rel g-top-1 g-mr-5"></i> Sign in
              </router-link>
            </li>
          </ul>
        </div>
      </nav>
    </div>
  </section>
</template>

<script>
import store from '../../store'
// 在 JQuery 中使用 axios 的话需要重新导入，不能使用 main.js 中定义的 Vue 全局属性 this.$axios
import axios from 'axios'

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
      this.$toasted.show('You have been logged out.', {icon: 'fingerprint'})
      this.$router.push('/login')
    }
  },
  mounted() {
    // 轮询 /api/users/<int:id>/notifications/ 请求用户的新通知
    $(function () {
      let since = 0
      let total_notifications_count = 0  // 总通知计数
      let unread_recived_comments_count = 0  // 收到的新评论通知计数
      let unread_messages_count = 0  // 收到的新私信通知计数
      let unread_follows_count = 0  // 新粉丝通知计数
      let unread_likes_count = 0  // 新的喜欢或赞的通知计数
      let unread_followeds_posts_count = 0  // 用户关注的人的新文章通知计数

      setInterval(function () {
        if (window.localStorage.getItem('madblog-token')) {
          // 如果用户已登录，才开始请求 API
          const payload = JSON.parse(atob(window.localStorage.getItem('madblog-token').split('.')[1]))
          const user_id = payload.user_id
          const path = `/api/users/${user_id}/notifications/?since=${since}`
          axios.get(path)
            .then((response) => {
              // handle success
              for (var i = 0; i < response.data.length; i++) {
                switch (response.data[i].name) {
                  case 'unread_recived_comments_count':
                    unread_recived_comments_count = response.data[i].payload
                    break

                  case 'unread_messages_count':
                    unread_messages_count = response.data[i].payload
                    break

                  case 'unread_follows_count':
                    unread_follows_count = response.data[i].payload
                    break

                  case 'unread_likes_count':
                    unread_likes_count = response.data[i].payload
                    break

                  case 'unread_followeds_posts_count':
                    unread_followeds_posts_count = response.data[i].payload
                    break
                }
                since = response.data[i].timestamp
              }

              total_notifications_count = unread_recived_comments_count + unread_messages_count + unread_follows_count + unread_likes_count + unread_followeds_posts_count
              // 每一次请求之后，根据 total_notifications_count 的值来显示或隐藏徽标
              $('#new_notifications_count').text(total_notifications_count)
              $('#new_notifications_count').css('visibility', total_notifications_count ? 'visible' : 'hidden');
            })
            .catch((error) => {
              // handle error
              console.error(error)
            })
        }
      }, 10000)
    })
  }
}
</script>
