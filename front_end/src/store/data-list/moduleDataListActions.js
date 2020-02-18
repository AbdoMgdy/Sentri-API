/*=========================================================================================
  File Name: moduleCalendarActions.js
  Description: Calendar Module Actions
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
==========================================================================================*/

import axios from "@/axios.js";

export default {
  addItem({ commit }, item) {
    commit("ADD_ITEM", item);
  },
  fetchDataListItems({ commit }) {
    return new Promise((resolve, reject) => {
      axios
        .get("orders")
        .then(response => {
          commit("SET_PRODUCTS", response.data);
          resolve(response);
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  fetchUsers({ commit }) {
    return new Promise((resolve, reject) => {
      axios
        .get("customers")
        .then(response => {
          commit("SET_USERS", response.data.users);

          resolve(response);
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  // fetchEventLabels({ commit }) {
  //   return new Promise((resolve, reject) => {
  //     axios.get("/api/apps/calendar/labels")
  //       .then((response) => {
  //         commit('SET_LABELS', response.data)
  //         resolve(response)
  //       })
  //       .catch((error) => { reject(error) })
  //   })
  // },
  updateItem({ commit }, item) {
    let bodyFormData = new FormData();
    bodyFormData.set("order_number", item.number);
    bodyFormData.set("order_status", item.status);
    return new Promise((resolve, reject) => {
      axios({
        method: "post",
        url:
          "https://cors-anywhere.herokuapp.com/https://rest-bot-dev.herokuapp.com/edit_order_status",
        data: bodyFormData,
        headers: {
          "Content-Type": "multipart/form-data"
        }
      })
        .then(response => {
          commit("UPDATE_PRODUCT", item);
          resolve(response);
        })
        .catch(error => {
          reject(error);
        });
    });
  },
  removeItem({ commit }, itemId) {
    return new Promise((resolve, reject) => {
      axios
        .delete(`/api/data-list/products/${itemId}`)
        .then(response => {
          commit("REMOVE_ITEM", itemId);
          resolve(response);
        })
        .catch(error => {
          reject(error);
        });
    });
  }
  // eventDragged({ commit }, payload) {
  //   return new Promise((resolve, reject) => {
  //     axios.post(`/api/apps/calendar/event/dragged/${payload.event.id}`, {payload: payload})
  //       .then((response) => {

  //         // Convert Date String to Date Object
  //         let event = response.data
  //         event.startDate = new Date(event.startDate)
  //         event.endDate = new Date(event.endDate)

  //         commit('UPDATE_EVENT', event)
  //         resolve(response)
  //       })
  //       .catch((error) => { reject(error) })
  //   })
  // },
};
