<!-- =========================================================================================
  File Name: AddNewDataSidebar.vue
  Description: Add New Data - Sidebar component
========================================================================================== -->

<template>
  <vs-sidebar
    click-not-close
    position-right
    parent="body"
    default-index="1"
    color="primary"
    class="add-new-data-sidebar items-no-padding"
    spacer
    v-model="isSidebarActiveLocal"
  >
    <div class="mt-6 flex items-center justify-between px-6">
      <h4>
        {{ Object.entries(this.data).length === 0 ? "ADD NEW" : "UPDATE" }} ITEM
      </h4>
      <feather-icon
        icon="XIcon"
        @click.stop="isSidebarActiveLocal = false"
        class="cursor-pointer"
      ></feather-icon>
    </div>
    <vs-divider class="mb-0"></vs-divider>

    <VuePerfectScrollbar
      class="scroll-area--data-list-add-new"
      :settings="settings"
      :key="$vs.rtl"
    >
      <div class="p-6">
        <!-- Number -->
        <vs-input
          disabled
          label="Number"
          v-model="dataNumber"
          class="mt-5 w-full"
          name="number"
          v-validate="'required'"
        />
        <span class="text-danger text-sm" v-show="errors.has('item-name')">{{
          errors.first("item-name")
        }}</span>

        <!-- Status -->
        <vs-select
          v-model="dataStatus"
          label="Stauts"
          class="mt-5 w-full"
          name="item-Status"
          v-validate="'required'"
        >
          <vs-select-item
            :key="item.value"
            :value="item.value"
            :text="item.text"
            v-for="item in status_choices"
          />
        </vs-select>
        <span
          class="text-danger text-sm"
          v-show="errors.has('item-category')"
          >{{ errors.first("item-category") }}</span
        >

        <!-- PRICE -->
        <vs-input
          disabled
          icon-pack="feather"
          icon="icon-credit-card"
          label="Price"
          v-model="dataPrice"
          class="mt-5 w-full"
          v-validate="{ required: true, regex: /\d+(\.\d+)?$/ }"
          name="item-price"
        />
      </div>
    </VuePerfectScrollbar>

    <div class="flex flex-wrap items-center p-6" slot="footer">
      <vs-button class="mr-6" @click="submitData">Submit</vs-button>
      <vs-button
        type="border"
        color="danger"
        @click="isSidebarActiveLocal = false"
        >Cancel</vs-button
      >
    </div>
  </vs-sidebar>
</template>

<script>
import VuePerfectScrollbar from "vue-perfect-scrollbar";

export default {
  props: {
    isSidebarActive: {
      type: Boolean,
      required: true
    },
    data: {
      type: Object,
      default: () => {}
    }
  },
  watch: {
    isSidebarActive(val) {
      if (!val) return;
      if (Object.entries(this.data).length === 0) {
        this.initValues();
        this.$validator.reset();
      } else {
        console.log(this.data);

        // let { user, time, number, total, status, items } = this.data;
        this.dataOrder = this.data.items;
        this.dataStatus = this.data.status;
        this.dataPrice = this.data.total;
        this.dataNumber = this.data.number;
      }
      // Object.entries(this.data).length === 0 ? this.initValues() : { this.dataId, this.dataName, this.dataCategory, this.dataOrder_status, this.dataPrice } = JSON.parse(JSON.stringify(this.data))
    }
  },
  data() {
    return {
      dataOrder: "",
      dataStatus: "",
      dataPrice: 0,
      dataNumber: 0,

      status_choices: [
        { text: "Pending", value: "Pending" },
        { text: "Out", value: "Out" },
        { text: "Canceled", value: "Canceled" },
        { text: "Delivered", value: "Delivered" }
      ],
      settings: {
        // perfectscrollbar settings
        maxScrollbarLength: 60,
        wheelSpeed: 0.6
      }
    };
  },
  computed: {
    isSidebarActiveLocal: {
      get() {
        return this.isSidebarActive;
      },
      set(val) {
        if (!val) {
          this.$emit("closeSidebar");
          // this.$validator.reset()
          // this.initValues()
        }
      }
    },
    isFormValid() {
      return (
        !this.errors.any() &&
        this.dataName &&
        this.dataCategory &&
        this.dataPrice > 0
      );
    }
  },
  methods: {
    initValues() {
      this.dataOrder = "";
      this.dataStatus = "Pending";
      this.dataPrice = 0;
    },
    submitData() {
      const obj = {
        number: this.dataNumber,
        status: this.dataStatus
      };
      console.log(obj.number);
      this.$store.dispatch("dataList/updateItem", obj).catch(err => {
        console.error(err);
      });

      this.$emit("closeSidebar");
    }
  },
  components: {
    VuePerfectScrollbar
  }
};
</script>

<style lang="scss" scoped>
.add-new-data-sidebar {
  ::v-deep .vs-sidebar--background {
    z-index: 52010;
  }

  ::v-deep .vs-sidebar {
    z-index: 52010;
    width: 400px;
    max-width: 90vw;

    .img-upload {
      margin-top: 2rem;

      .con-img-upload {
        padding: 0;
      }

      .con-input-upload {
        width: 100%;
        margin: 0;
      }
    }
  }
}

.scroll-area--data-list-add-new {
  // height: calc(var(--vh, 1vh) * 100 - 4.3rem);
  height: calc(var(--vh, 1vh) * 100 - 16px - 45px - 82px);
}
</style>
