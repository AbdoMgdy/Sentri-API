/*=========================================================================================
  File Name: store.js
  Description: Vuex store
==========================================================================================*/

import Vue from "vue";
import Vuex from "vuex";

import state from "./state";
import getters from "./getters";
import mutations from "./mutations";
import actions from "./actions";

Vue.use(Vuex);

import moduleDataList from "./data-list/moduleDataList";

export default new Vuex.Store({
  getters,
  mutations,
  state,
  actions,
  modules: {
    dataList: moduleDataList
  },
  strict: process.env.NODE_ENV !== "production"
});
