// 使用 `import` 命令加载的 Vue 构建版本
//（仅运行时或独立）已在 webpack.base.conf 中设置了别名。
import Vue from 'vue' // 引入vue
import App from './App' // 引入App.vue
import router from './router' // 引入路由
// 引入bootstrap
import 'bootstrap/dist/css/bootstrap.css'

Vue.config.productionTip = false  // 关闭生产模式下的提示

/* eslint-disable no-new */
new Vue({ // 创建一个 Vue 实例
  el: '#app', // 挂载到 #app 元素
  router, // 挂载路由
  components: {App},  // 挂载组件
  template: '<App/>'  // 挂载模板
})
