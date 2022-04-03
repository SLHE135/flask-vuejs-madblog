<template>
  <div class="container">
    <button class="btn btn-primary" type="button">{{ msg }}</button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Ping',
  data() {
    return {
      msg: 'Hello, This is Ping.vue component'
    }
  },
  //methods是一个对象，里面的方法可以被组件内部调用
  methods: {
    getMessage() {  //获取消息
      const path = 'http://localhost:5000/api/ping' //接口地址
      axios.get(path).then(response => {  //axios.get()方法是一个异步方法，返回一个promise对象
        this.msg = response.data; //获取接口返回的数据
      }).catch(error => { //catch方法是一个promise对象的方法，用来捕获promise对象的错误
        console.error(error); //打印错误信息
      })
    }
  },
  created() {// created()是一个钩子函数，组件创建完成后调用
    this.getMessage() //调用getMessage()方法
  }
}
</script>
