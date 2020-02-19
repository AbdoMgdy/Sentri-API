<!-- =========================================================================================
File Name: RegisterJWT.vue
Description: Register Page for JWT
----------------------------------------------------------------------------------------
Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
Author URL: http://www.themeforest.net/user/pixinvent
========================================================================================== -->

<template>
  <div class="clearfix">
    <vs-input
      v-validate="'required|alpha_dash|min:3'"
      data-vv-validate-on="blur"
      label-placeholder="Name"
      name="displayName"
      placeholder="Name"
      v-model="displayName"
      class="w-full"
    />
    <span class="text-danger text-sm">{{ errors.first("displayName") }}</span>

    <vs-input
      v-validate="'required'"
      data-vv-validate-on="blur"
      name="page_id"
      label-placeholder="Page Id"
      placeholder="Page Id"
      v-model="page_id"
      class="w-full mt-6"
    />
    <span class="text-danger text-sm">{{ errors.first("page_id") }}</span>
    <vs-input
      v-validate="'required'"
      data-vv-validate-on="blur"
      name="access_token"
      label-placeholder="Access Token"
      placeholder="Access Token"
      v-model="access_token"
      class="w-full mt-6"
    />
    <span class="text-danger text-sm">{{ errors.first("access_token") }}</span>

    <vs-input
      ref="password"
      type="password"
      data-vv-validate-on="blur"
      v-validate="'required|min:6|max:10'"
      name="password"
      label-placeholder="Password"
      placeholder="Password"
      v-model="password"
      class="w-full mt-6"
    />
    <span class="text-danger text-sm">{{ errors.first("password") }}</span>

    <vs-input
      type="password"
      v-validate="'min:6|max:10|confirmed:password'"
      data-vv-validate-on="blur"
      data-vv-as="password"
      name="confirm_password"
      label-placeholder="Confirm Password"
      placeholder="Confirm Password"
      v-model="confirm_password"
      class="w-full mt-6"
    />
    <span class="text-danger text-sm">{{
      errors.first("confirm_password")
    }}</span>

    <vs-button type="border" @click="logout" class="mt-6">Logout</vs-button>
    <vs-button
      class="float-right mt-6"
      @click="registerUserJWt"
      :disabled="!validateForm"
      >Register</vs-button
    >
  </div>
</template>

<script>
export default {
  data() {
    return {
      displayName: "",
      page_id: "",
      access_token: "",
      password: "",
      confirm_password: ""
    };
  },
  computed: {
    validateForm() {
      return (
        !this.errors.any() &&
        this.displayName != "" &&
        this.page_id != "" &&
        this.access_token != "" &&
        this.password != "" &&
        this.confirm_password != ""
      );
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
    logout() {
      localStorage.removeItem("accessToken");
      this.$store.dispatch("logoutUser");
    },
    registerUserJWt() {
      // If form is not validated or user is already login return
      if (!this.validateForm || !this.checkLogin()) return;

      const payload = {
        userDetails: {
          displayName: this.displayName,
          page_id: this.page_id,
          access_token: this.access_token,
          password: this.password,
          confirmPassword: this.confirm_password
        },
        notify: this.$vs.notify
      };
      this.$store.dispatch("auth/registerUserJWT", payload);
    }
  }
};
</script>
