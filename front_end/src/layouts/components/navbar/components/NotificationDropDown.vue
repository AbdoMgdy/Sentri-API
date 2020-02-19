<template>
  <!-- NOTIFICATIONS -->
  <vs-dropdown vs-custom-content vs-trigger-click class="cursor-pointer">
    <feather-icon
      icon="BellIcon"
      class="cursor-pointer mt-1 sm:mr-6 mr-2"
      :badge="unreadNotifications.length"
    />

    <vs-dropdown-menu
      class="notification-dropdown dropdown-custom vx-navbar-dropdown"
    >
      <div class="notification-top text-center p-5 bg-primary text-white">
        <h3 class="text-white">{{ unreadNotifications.length }} New</h3>
        <p class="opacity-75">Orders</p>
      </div>

      <VuePerfectScrollbar
        ref="mainSidebarPs"
        class="scroll-area--nofications-dropdown p-0 mb-10"
        :settings="settings"
        :key="$vs.rtl"
      >
        <ul class="bordered-items">
          <li
            v-for="ntf in unreadNotifications"
            :key="ntf.index"
            class="flex justify-between px-4 py-4 notification cursor-pointer"
            @click="removeNtf(ntf.index)"
          >
            <div class="flex items-start">
              <feather-icon
                :icon="ntf.icon"
                :svgClasses="[
                  `text-${ntf.category}`,
                  'stroke-current mr-1 h-6 w-6'
                ]"
              ></feather-icon>
              <div class="mx-2">
                <span
                  class="font-medium block notification-title"
                  :class="[`text-${ntf.category}`]"
                  >{{ ntf.title }}</span
                >
                <small>{{ ntf.msg }} {{ $socket.connected }}</small>
              </div>
            </div>
            <!-- <small class="mt-1 whitespace-no-wrap">{{
              elapsedTime(ntf.time)
            }}</small> -->
          </li>
        </ul>
      </VuePerfectScrollbar>

      <div
        class="
        checkout-footer
        fixed
        bottom-0
        rounded-b-lg
        text-primary
        w-full
        p-2
        font-semibold
        text-center
        border
        border-b-0
        border-l-0
        border-r-0
        border-solid
        d-theme-border-grey-light
        cursor-pointer"
        @click="clearNtfs"
      >
        <span>Clear Notifications</span>
      </div>
    </vs-dropdown-menu>
  </vs-dropdown>
</template>

<script>
import VuePerfectScrollbar from "vue-perfect-scrollbar";

export default {
  components: {
    VuePerfectScrollbar
  },
  data() {
    return {
      noOfRepetitions: 5,
      ntfSound: new Audio(
        "https://cdn.jsdelivr.net/npm/ion-sound@3.0.7/sounds/bell_ring.mp3"
      ),
      unreadNotifications: [],
      settings: {
        maxScrollbarLength: 60,
        wheelSpeed: 0.6
      }
    };
  },
  sockets: {
    connect() {
      console.log("Ntf Socket Connected");
    },
    order(data) {
      console.log(data);
      let vm = this;
      let timer = setInterval(function() {
        vm.ntfSound.play();
      }, 3000);
      this.$vs.notify({
        title: "New Order Recieved",
        text: "You got new order of goods.",
        icon: "notifications",
        position: "top-center",
        fixed: true,
        click: () => {
          clearInterval(timer);
        }
      });
      this.unreadNotifications.push({
        index: 0,
        title: "New Order Recieved",
        msg: "You got new order of goods.",
        icon: "PackageIcon",
        time: new Date(),
        category: "primary"
      });
    }
  },
  methods: {
    elapsedTime(startTime) {
      let x = new Date(startTime);
      let now = new Date();
      var timeDiff = now - x;
      timeDiff /= 1000;
      console.log(timeDiff);

      var seconds = Math.round(timeDiff);
      timeDiff = Math.floor(timeDiff / 60);

      var minutes = Math.round(timeDiff % 60);
      timeDiff = Math.floor(timeDiff / 60);

      var hours = Math.round(timeDiff % 24);
      timeDiff = Math.floor(timeDiff / 24);

      var days = Math.round(timeDiff % 365);
      timeDiff = Math.floor(timeDiff / 365);

      var years = timeDiff;

      if (years > 0) {
        return years + (years > 1 ? " Years " : " Year ") + "ago";
      } else if (days > 0) {
        return days + (days > 1 ? " Days " : " Day ") + "ago";
      } else if (hours > 0) {
        return hours + (hours > 1 ? " Hrs " : " Hour ") + "ago";
      } else if (minutes > 0) {
        return minutes + (minutes > 1 ? " Mins " : " Min ") + "ago";
      } else if (seconds > 0) {
        return seconds + (seconds > 1 ? " sec ago" : "just now");
      }

      return "Just Now";
    },
    // Method for creating dummy notification time
    randomDate({ hr, min, sec }) {
      let date = new Date();

      if (hr) date.setHours(date.getHours() - hr);
      if (min) date.setMinutes(date.getMinutes() - min);
      if (sec) date.setSeconds(date.getSeconds() - sec);

      return date;
    },
    removeNtf(index) {
      this.unreadNotifications.splice(index, 1);
    },
    clearNtfs() {
      this.unreadNotifications.splice(0, this.unreadNotifications.length);
    }
  }
};
</script>
