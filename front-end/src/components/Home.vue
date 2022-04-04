<template>
  <div class="container">
    <alert
      v-for="(alert, index) in alerts" :key="index"
      v-bind:message="alert.message"
      v-bind:variant="alert.variant">
    </alert>
    <button class="btn btn-primary" type="button">HomePage</button>
  </div>
</template>

<script>
import Alert from './Alert'

export default {
  name: 'Home',  //this is the name of the component
  components: {
    alert: Alert
  },
  data() {
    return {
      alerts: [
        {
          variant: 'info',
          message: 'Hi'
        },
        {
          variant: 'danger',
          message: 'Oops..'
        },
        {
          variant: 'success',
          message: 'OK'
        }
      ]
    }
  }
}
</script>
