/*=========================================================================================
  File Name: moduleCalendarMutations.js
  Description: Calendar Module Mutations

==========================================================================================*/

export default {
  ADD_ITEM(state, item) {
    item.time = new Date(item.time);
    state.products.unshift(item);
  },
  SET_PRODUCTS(state, products) {
    const productsMap = products.map(el => {
      el.time = new Date(el.time);
      return el;
    });
    state.products = productsMap;
  },
  SET_USERS(state, users) {
    state.users = users;
  },
  // SET_LABELS(state, labels) {
  //   state.eventLabels = labels
  // },
  UPDATE_PRODUCT(state, product) {
    const productIndex = state.products.findIndex(
      p => p.number == product.number
    );
    state.products[productIndex].status = product.status;
  },
  REMOVE_ITEM(state, itemId) {
    const ItemIndex = state.products.findIndex(p => p.id == itemId);
    state.products.splice(ItemIndex, 1);
  }
};
