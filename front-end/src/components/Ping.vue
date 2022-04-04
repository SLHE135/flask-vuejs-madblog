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
      msg: ''
    }
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/api/ping'
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        })
    }
  },
  created() {
    this.getMessage()
  }
}
</script>
