<template>
  <div>
    <h1>Add Role</h1>
    <form @submit.prevent="onSubmit">
      <div class="form-group" v-bind:class="{'u-has-error-v1': roleForm.slugError}">
        <label for="slug">Slug</label>
        <input id="slug" v-model="roleForm.slug" class="form-control" placeholder="" type="text">
        <small v-show="roleForm.slugError" class="form-control-feedback">{{ roleForm.slugError }}</small>
      </div>
      <div class="form-group" v-bind:class="{'u-has-error-v1': roleForm.nameError}">
        <label for="name">Name</label>
        <input id="name" v-model="roleForm.name" class="form-control" placeholder="" type="text">
        <small v-show="roleForm.nameError" class="form-control-feedback">{{ roleForm.nameError }}</small>
      </div>
      <div class="form-group">
        <label for="permissions">Permissions</label>
        <div>
          <!-- Inline Checkboxes -->
          <div v-for="(perm, index) in perms" v-bind:key="index" class="form-check form-check-inline mb-0">
            <label class="form-check-label mr-2">
              <input v-bind:id="perm.dec" v-model="checkPerms" class="form-check-input mr-1" type="checkbox"
                     v-bind:value="perm.dec">{{ perm.name }}
            </label>
          </div>
          <!-- End Inline Checkboxes -->
        </div>
      </div>
      <button class="btn btn-primary" type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
import store from '../../store'

export default {
  name: 'AddRole',  //this is the name of the component
  data() {
    return {
      sharedState: store.state,
      roleForm: {
        slug: '',
        name: '',
        permissions: [],
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        slugError: null,
        nameError: null
      },
      perms: null,
      checkPerms: []
    }
  },
  methods: {
    getPerms() {
      const path = `/api/roles/perms`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.perms = response.data
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onSubmit(e) {
      this.roleForm.errors = 0  // 重置

      if (!this.roleForm.slug) {
        this.roleForm.errors++
        this.roleForm.slugError = 'Slug required.'
      } else {
        this.roleForm.slugError = null
      }

      if (!this.roleForm.name) {
        this.roleForm.errors++
        this.roleForm.nameError = 'Role name required.'
      } else {
        this.roleForm.nameError = null
      }

      if (this.roleForm.errors > 0) {
        // 如果slug或name为空时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      const path = `/api/roles`
      const payload = {
        slug: this.roleForm.slug,
        name: this.roleForm.name,
        permissions: this.checkPerms
      }
      this.$axios.post(path, payload)
        .then((response) => {
          // handle success
          this.$toasted.success('Successed add a new role.', {icon: 'fingerprint'})
          this.$router.push({name: 'AdminRoles'})
        })
        .catch((error) => {
          // handle error
          for (var field in error.response.data.message) {
            if (field == 'slug') {
              this.roleForm.slugError = error.response.data.message[field]
            } else if (field == 'name') {
              this.roleForm.nameError = error.response.data.message[field]
            } else {
              this.$toasted.error(error.response.data.message[field], {icon: 'fingerprint'})
            }
          }
        })
    }
  },
  created() {
    this.getPerms()
  },
}
</script>
