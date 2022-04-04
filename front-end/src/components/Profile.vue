<template>
  <div class="container">
    <alert
      v-if="showAlert"
      v-bind:message="alertMessage"
      v-bind:variant="alertVariant">
    </alert>
    <button class="btn btn-primary" type="button">ProfilePage</button>
  </div>
</template>

<script>
import Alert from './Alert'

export default {
  name: 'Profile',  //this is the name of the component
  components: {
    alert: Alert
  },
  data() {
    return {
      showAlert: true,
      alertVariant: 'danger',
      alertMessage: 'You can see me when you have sign in'
    }
  }
}
</script>
