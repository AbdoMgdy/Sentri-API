/*=========================================================================================
  File Name: moduleAuthActions.js
  Description: Auth Module Actions

==========================================================================================*/

import jwt from "../../http/requests/auth/jwt/index.js";
import store from "../../store/store";
import router from "@/router";

export default {
  // JWT
  loginJWT({ commit }, payload) {
    return new Promise((resolve, reject) => {
      jwt
        .login(payload.userDetails.username, payload.userDetails.password)
        .then(response => {
          console.log(response);
          // If there's user data in response
          if (response.data.userData) {
            console.log(response);
            store.dispatch("loginUser");
            // Set accessToken
            localStorage.setItem("accessToken", response.data.accessToken);

            // Update user details
            commit("UPDATE_USER_INFO", response.data.userData, { root: true });

            // Set bearer token in axios
            commit("SET_BEARER", response.data.accessToken);

            // Navigate User to homepage
            router.push({ path: "/" });
            resolve(response);
          } else {
            reject({ message: "Wrong Usernmae or Password" });
          }
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  registerUserJWT({ commit }, payload) {
    const {
      displayName,
      page_id,
      access_token,
      password,
      confirmPassword
    } = payload.userDetails;

    return new Promise((resolve, reject) => {
      // Check confirm password
      if (password !== confirmPassword) {
        reject({ message: "Password doesn't match. Please try again." });
      }

      jwt
        .registerUser(displayName, password, page_id, access_token)
        .then(response => {
          // Redirect User
          router.push(router.currentRoute.query.to || "/");

          // Update data in localStorage
          localStorage.setItem("accessToken", response.data.accessToken);
          commit("UPDATE_USER_INFO", response.data.userData, { root: true });

          resolve(response);
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  fetchAccessToken() {
    return new Promise(resolve => {
      jwt.refreshToken().then(response => {
        resolve(response);
      });
    });
  }
};
