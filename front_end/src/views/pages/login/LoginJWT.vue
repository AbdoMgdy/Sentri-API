<template>
  <div>
    <vs-input
      v-validate="'required|min:3'"
      data-vv-validate-on="blur"
      name="username"
      icon-no-border
      icon="icon icon-user"
      icon-pack="feather"
      label-placeholder="Username"
      v-model="username"
      class="w-full"
    />
    <span class="text-danger text-sm">{{ errors.first("username") }}</span>

    <vs-input
      data-vv-validate-on="blur"
      v-validate="'required|min:6|max:10'"
      type="password"
      name="password"
      icon-no-border
      icon="icon icon-lock"
      icon-pack="feather"
      label-placeholder="Password"
      v-model="password"
      class="w-full mt-6"
    />
    <span class="text-danger text-sm">{{ errors.first("password") }}</span>

    <!-- <div class="flex flex-wrap justify-between my-5" style="display:none">
      <vs-checkbox v-model="checkbox_remember_me" class="mb-3"
        >Remember Me</vs-checkbox
      >
    </div> -->
    <div class="flex flex-wrap justify-between mb-3 mt-5">
      <vs-button :disabled="!validateForm" @click="loginJWT">Login</vs-button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
      checkbox_remember_me: false
    };
  },
  computed: {
    validateForm() {
      return !this.errors.any() && this.email != "" && this.password != "";
    }
  },
  methods: {
    checkLogin() {
      // If user is already logged in notify
      if (this.$store.getters.AppActiveUser.isLoggedIn) {
        // Close animation if passed as payload
        // this.$vs.loading.close()

        this.$vs.notify({
          title: "Login Attempt",
          text: "You are already logged in!",
          iconPack: "feather",
          icon: "icon-alert-circle",
          color: "warning"
        });

        return false;
      }
      return true;
    },
    loginJWT() {
      // if (!this.checkLogin()) return; Uncomment This in production

      // Loading
      this.$vs.loading();

      const payload = {
        checkbox_remember_me: this.checkbox_remember_me,
        userDetails: {
          username: this.username,
          password: this.password
        }
      };

      this.$store
        .dispatch("auth/loginJWT", payload)
        .then(response => {
          console.log(response);
          this.$vs.loading.close();
        })
        .catch(error => {
          console.log(error);
          this.$vs.loading.close();
          this.$vs.notify({
            title: "Error",
            text: error.message,
            iconPack: "feather",
            icon: "icon-alert-circle",
            color: "danger"
          });
        });
    },
    registerUser() {
      if (!this.checkLogin()) return;
      this.$router.push("/pages/register").catch(() => {});
    }
  }
};
</script>
