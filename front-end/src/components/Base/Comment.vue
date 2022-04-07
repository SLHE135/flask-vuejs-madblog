<template>
  <div class="media g-mb-20">
    <router-link v-bind:title="comment.author.name || comment.author.username"
                 v-bind:to="{ path: `/user/${comment.author.id}` }">
      <img class="d-flex g-width-50 g-height-50 rounded-circle g-mt-3 g-mr-20"
           v-bind:alt="comment.author.name || comment.author.username" v-bind:src="comment.author.avatar">
    </router-link>
    <div class="media-body g-brd-around g-brd-gray-light-v4 g-brd-left-1 g-pa-20" v-bind:class="leftBrdColor">
      <div class="d-sm-flex justify-content-sm-between align-items-sm-center g-mb-15 g-mb-10--sm">
        <h5 v-if="comment.author.id == comment.post.author_id"
            class="h4 g-font-weight-300 g-mr-10 g-mb-5 g-mb-0--sm g-color-pink"><span
          class="g-mr-5">{{ comment.author.name || comment.author.username }}</span>
          <button class="btn btn-xs u-btn-inset u-btn-outline-red g-mr-5">博文作者</button>
        </h5>
        <h5 v-else class="h4 g-font-weight-300 g-mr-10 g-mb-5 g-mb-0--sm">
          {{ comment.author.name || comment.author.username }}</h5>
        <div class="text-nowrap g-font-size-12">
          <span>{{ $moment(comment.timestamp).fromNow() }}</span> / <a href="javascript:;">Reply</a>
        </div>
      </div>

      <!-- vue-markdown 开始解析markdown，它是子组件，通过 props 给它传值即可
      v-highlight 是自定义指令，用 highlight.js 语法高亮 -->
      <vue-markdown
        v-highlight
        :source="comment.body"
        class="markdown-body g-mb-15">
      </vue-markdown>

      <div class="d-flex justify-content-start">
        <ul class="list-inline mb-0">
          <li class="list-inline-item g-mr-20">
            <a class="g-color-gray-dark-v5 g-text-underline--none--hover" href="javascript:;">
              <i class="icon-like g-pos-rel g-top-1 g-mr-3"></i> 0
            </a>
          </li>
          <li class="list-inline-item g-mr-20">
            <a class="g-color-gray-dark-v5 g-text-underline--none--hover" href="javascript:;">
              <i class="icon-dislike g-pos-rel g-top-1 g-mr-3"></i> 0
            </a>
          </li>
          <!-- 该评论发表在哪篇博客文章下面 -->
          <li class="list-inline-item g-mr-20">
            <router-link class="g-color-gray-dark-v5 g-text-underline--none--hover"
                         v-bind:to="{ name: 'PostDetail', params: { id: comment.post.id } }">
              <i class="icon-share g-pos-rel g-top-1 g-mr-3"></i>
            </router-link>
          </li>
        </ul>
        <ul class="list-inline mb-0 ml-auto">
          <li v-if="comment.author.id == sharedState.user_id" class="list-inline-item g-mr-5">
            <button class="btn btn-xs u-btn-outline-purple" data-target="#editCommentModal" data-toggle="modal"
                    v-on:click="$emit('edit-comment')">编辑
            </button>
          </li>
          <li v-if="comment.author.id == sharedState.user_id" class="list-inline-item">
            <button class="btn btn-xs u-btn-outline-red" v-on:click="$emit('delete-comment')">删除</button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import store from '../../store'
// 导入 vue-markdown 组件解析 markdown 原文为　HTML
import VueMarkdown from 'vue-markdown'

export default {
  props: ['comment'],
  components: {
    VueMarkdown
  },
  data() {
    return {
      sharedState: store.state
    }
  },
  computed: {
    leftBrdColor: function () {
      const colors = ['primary', 'blue', 'red', 'purple', 'orange', 'yellow', 'aqua', 'cyan', 'teal', 'brown', 'pink', 'black']
      let index = Math.floor((Math.random() * colors.length))
      return 'g-brd-' + colors[index] + '-left'
    }
  }
}
</script>
