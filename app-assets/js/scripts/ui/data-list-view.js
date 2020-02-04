/*=========================================================================================
    File Name: data-list-view.js
    Description: List View
    ----------------------------------------------------------------------------------------
    Item Name: Vuexy  - Vuejs, HTML & Laravel Admin Dashboard Template
    Author: PIXINVENT
==========================================================================================*/

$(document).ready(function() {
  "use strict"
  // init list view datatable
  var dataListView = $(".data-list-view").DataTable({
    responsive: false,
    columnDefs: [
      {
        orderable: true,
        targets: 0,
      }
    ],
    dom:
      '<"top"<"actions action-btns"B><"action-filters"lf>><"clear">rt<"bottom"<"actions">p>',
    oLanguage: {
      sLengthMenu: "_MENU_",
      sSearch: ""
    },
    aLengthMenu: [[-1, 10, 15, 20], ["All", 10, 15, 20]],
    select: {
      style: "single"
    },
    order: [[1, "asc"]],
    bInfo: false,
    pageLength: 4,
    buttons: [{
    }],
    initComplete: function(settings, json) {
      $(".dt-buttons .btn").removeClass("btn-secondary")
    }
  });

  dataListView.on('draw.dt', function(){
    setTimeout(function(){
      if (navigator.userAgent.indexOf("Mac OS X") != -1) {
        $(".dt-checkboxes-cell input, .dt-checkboxes").addClass("mac-checkbox")
      }
    }, 50);
  });

  // To append actions dropdown before add new button
  var actionDropdown = $(".actions-dropodown")
  actionDropdown.insertBefore($(".top .actions .dt-buttons"))


  // Scrollbar
  if ($(".data-items").length > 0) {
    new PerfectScrollbar(".data-items", { wheelPropagation: false })
  }

  // Close sidebar
  $(".hide-data-sidebar,  .cancel-data-btn, .overlay-bg").on("click", function() {
    $(".add-new-data").removeClass("show")
    $(".overlay-bg").removeClass("show")
    $("#data-name, #data-price").val("")
    $("#data-category, #data-status").prop("selectedIndex", 0)
  })

  var row;
  var bodyFormData = new FormData()
  // On Edit
  $('.data-list-view').on("click", function (e) {
    console.log(e.target)
    
    row = e.target.parentNode.parentNode.parentNode;
    console.log(row)
    if (e.target.className === '.action-edit') {
      $('#data-name').val(row.children[2].textContent);
      $('#data-tel').val(row.children[3].textContent);
      $('#data-price').val(row.children[7].textContent);
      $('#data-status').val(row.children[5].children[0].children[0].children[0].textContent);
      $(".add-new-data").addClass("show");
      $(".overlay-bg").addClass("show");
    }
  });

  // On Confirm
  $('.action-confirm').on("click", function (e) {
    e.stopPropagation();
    if ($('#data-status').val() === "Pending") {
      row.children[5].children[0].setAttribute("class", "chip chip-info")
      row.children[5].children[0].children[0].children[0].textContent = $('#data-status').val();
      $(".add-new-data").removeClass("show")
      $(".overlay-bg").removeClass("show")
      bodyFormData.set('order_number', row.children[1].textContent);
      bodyFormData.set('order_status', row.children[5].children[0].children[0].children[0].textContent);
    } else if ($('#data-status').val() === "Out") { 
      row.children[5].children[0].setAttribute("class", "chip chip-warning")
      row.children[5].children[0].children[0].children[0].textContent = $('#data-status').val();
      $(".add-new-data").removeClass("show")
      $(".overlay-bg").removeClass("show")
      bodyFormData.set('order_number', row.children[1].textContent);
      bodyFormData.set('order_status', row.children[5].children[0].children[0].children[0].textContent);
    } else if ($('#data-status').val() === "Canceled") { 
      row.children[5].children[0].setAttribute("class", "chip chip-danger")
      row.children[5].children[0].children[0].children[0].textContent = $('#data-status').val();
      $(".add-new-data").removeClass("show")
      $(".overlay-bg").removeClass("show")
      bodyFormData.set('order_number', row.children[1].textContent);
      bodyFormData.set('order_status', row.children[5].children[0].children[0].children[0].textContent);
    } else {
      row.children[5].children[0].setAttribute("class", "chip chip-success")
      row.children[5].children[0].children[0].children[0].textContent = $('#data-status').val();
      $(".add-new-data").removeClass("show")
      $(".overlay-bg").removeClass("show")
      bodyFormData.set('order_number', row.children[1].textContent);
      bodyFormData.set('order_status', row.children[5].children[0].children[0].children[0].textContent);
    }

    sendOrderStatus(bodyFormData)
    
  });
    var sendOrderStatus =  function (bodyFormData) {
    axios({
      method: 'post',
      url: '/edit_order_status',
      data: bodyFormData,
      headers: { 'Content-Type': 'multipart/form-data' }
    })
      .then(function (response) {
        //handle success
        return
      })
      .catch(function (err) {
        //handle error
        console.log(err);
      })
  };

  // mac chrome checkbox fix
  if (navigator.userAgent.indexOf("Mac OS X") != -1) {
    $(".dt-checkboxes-cell input, .dt-checkboxes").addClass("mac-checkbox")
  }
})
