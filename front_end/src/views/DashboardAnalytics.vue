<!-- =========================================================================================
  File Name: DashboardAnalytics.vue
  Description: Dashboard Analytics
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
========================================================================================== -->

<template>
  <div id="dashboard-analytics">
    <div class="vx-row">
      <!-- CARD 1: Product Orders -->
      <div class="vx-col w-full lg:w-1/3 mb-base">
        <vx-card title="Orders">
          <!-- CARD ACTION -->
          <template slot="actions"> </template>

          <!-- Chart -->
          <div slot="no-body">
            <vue-apex-charts
              type="radialBar"
              height="300"
              :options="analyticsData.productOrdersRadialBar.chartOptions"
              :series="series"
            />
          </div>
          <ul>
            <li class="flex mb-3 justify-between">
              <span class="flex items-center">
                <span
                  class="inline-block h-4 w-4 rounded-full mr-2 bg-white border-3 border-solid border-primary"
                ></span>
                <span class="font-semibold">Pending</span>
              </span>
              <span
                ><animated-number round="1" :value="orders.pending.length"
              /></span>
            </li>
            <li class="flex mb-3 justify-between">
              <span class="flex items-center">
                <span
                  class="inline-block h-4 w-4 rounded-full mr-2 bg-white border-3 border-solid border-warning"
                ></span>
                <span class="font-semibold">Out</span>
              </span>
              <span
                ><animated-number round="1" :value="orders.out.length"
              /></span>
            </li>
            <li class="flex mb-3 justify-between">
              <span class="flex items-center">
                <span
                  class="inline-block h-4 w-4 rounded-full mr-2 bg-white border-3 border-solid border-danger"
                ></span>
                <span class="font-semibold">Canceled</span>
              </span>
              <span
                ><animated-number round="1" :value="orders.canceled.length"
              /></span>
            </li>
            <li class="flex mb-3 justify-between">
              <span class="flex items-center">
                <span
                  class="inline-block h-4 w-4 rounded-full mr-2 bg-white border-3 border-solid border-success"
                ></span>
                <span class="font-semibold">Delivered</span>
              </span>
              <span
                ><animated-number round="1" :value="orders.delivered.length"
              /></span>
            </li>
          </ul>
        </vx-card>
      </div>

      <div class="vx-col w-full sm:w-1/2 md:w-1/2 lg:w-1/4 xl:w-1/4 mb-base">
        <!-- CARD 2: SUBSCRIBERS GAINED -->
        <statistics-card-line
          icon="UsersIcon"
          :statistic="users"
          statisticTitle="Subscribers Gained"
          :chartData="subscribersGained.series"
          type="area"
        ></statistics-card-line>
        <!-- CARD 3: ORDER RECIEVED -->
        <statistics-card-line
          class="mt-5"
          icon="ShoppingBagIcon"
          :statistic="products.length"
          statisticTitle="Orders Received"
          :chartData="subscribersGained.series"
          color="warning"
          type="area"
        ></statistics-card-line>
      </div>
      <div class="vx-col w-full sm:w-1/2 md:w-1/2 lg:w-1/4 xl:w-1/4 mb-base">
        <vx-card title="Choose Date">
          <flat-pickr
            :config="configFromdateTimePicker"
            v-model="fromDate"
            placeholder="From Date"
            @on-change="onFromChange"
          />
          <flat-pickr
            :config="configTodateTimePicker"
            v-model="toDate"
            placeholder="To Date"
            @on-change="onToChange"
          />
        </vx-card>
      </div>
    </div>
  </div>
</template>

<script>
import AnimatedNumber from "animated-number-vue";
import VueApexCharts from "vue-apexcharts";
import flatPickr from "vue-flatpickr-component";
import "flatpickr/dist/flatpickr.css";
import StatisticsCardLine from "@/components/statistics-cards/StatisticsCardLine.vue";
import analyticsData from "./ui-elements/card/analyticsData.js";

export default {
  data() {
    return {
      fromDate: "2020-01-01",
      toDate: new Date(),
      configFromdateTimePicker: {
        minDate: null,
        maxDate: null
      },
      configTodateTimePicker: {
        minDate: null
      },
      checkpointReward: {},
      subscribersGained: {},
      ordersRecevied: {},
      salesBarSession: {},
      supportTracker: {},
      productsOrder: {},
      salesRadar: {},

      analyticsData,
      dispatchedOrders: []
    };
  },
  components: {
    AnimatedNumber,
    VueApexCharts,
    StatisticsCardLine,
    flatPickr
  },
  computed: {
    users() {
      return this.$store.state.dataList.users;
    },
    products() {
      return this.$store.state.dataList.products.filter(el => {
        if (
          el.time >= Date.parse(this.fromDate) &&
          el.time <= Date.parse(this.toDate)
        ) {
          return true;
        } else {
          return false;
        }
      });
    },
    orders() {
      let orders = this.products;
      return {
        pending: orders.filter(el => el.status == "Pending"),
        out: orders.filter(el => el.status == "Out"),
        canceled: orders.filter(el => el.status == "Canceled"),
        delivered: orders.filter(el => el.status == "Delivered")
      };
    },
    series() {
      const pending = this.orders.pending.length;
      const out = this.orders.out.length;
      const canceled = this.orders.canceled.length;
      const delivered = this.orders.delivered.length;
      const total = pending + out + canceled + delivered;
      const deliveredPercentage = Math.round((delivered / total) * 100);
      const outPercentage = Math.round((out / total) * 100);
      const pendingPercentage = Math.round((pending / total) * 100);
      const canceledPercentage = Math.round((canceled / total) * 100);
      return [
        deliveredPercentage,
        canceledPercentage,
        outPercentage,
        pendingPercentage
      ];
    }
  },
  methods: {
    onFromChange(selectedDates, dateStr) {
      this.$set(this.configTodateTimePicker, "minDate", dateStr);
    },
    onToChange(selectedDates, dateStr) {
      this.$set(this.configFromdateTimePicker, "maxDate", dateStr);
    }
  }
};
</script>

<style lang="scss">
/*! rtl:begin:ignore */
#dashboard-analytics {
  .greet-user {
    position: relative;

    .decore-left {
      position: absolute;
      left: 0;
      top: 0;
    }
    .decore-right {
      position: absolute;
      right: 0;
      top: 0;
    }
  }

  @media (max-width: 576px) {
    .decore-left,
    .decore-right {
      width: 140px;
    }
  }
}
/*! rtl:end:ignore */
</style>
