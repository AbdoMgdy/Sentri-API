/*=========================================================================================
    File Name: data-list-view.js
    Description: List View
==========================================================================================*/

$(document).ready(function () {
  "use strict"
  // init list view datatable
  var dataListView = $(".data-list-view").DataTable({
    responsive: false,
    columnDefs: [{
      orderable: true,
      targets: 0,
    }],
    dom: '<"top"<"actions action-btns"B><"action-filters"lf>><"clear">rt<"bottom"<"actions">p>',
    oLanguage: {
      sLengthMenu: "_MENU_",
      sSearch: ""
    },
    aLengthMenu: [
      [5, 1, 15, -1],
      [5, 10, 15, "All"]
    ],
    select: {
      style: "single"
    },
    order: [
      [1, "asc"]
    ],
    bInfo: false,
    pageLength: 5,
    buttons: [{}],
    initComplete: function (settings, json) {
      $(".dt-buttons .btn").removeClass("btn-secondary")
    }
  });

  dataListView.on('draw.dt', function () {
    setTimeout(function () {
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
    new PerfectScrollbar(".data-items", {
      wheelPropagation: false
    })
  }

  // Close sidebar
  $(".hide-data-sidebar,  .cancel-data-btn, .overlay-bg").on("click", function () {
    $(".add-new-data").removeClass("show")
    $(".overlay-bg").removeClass("show")
    $("#data-name, #data-price").val("")
    $("#data-category, #data-status").prop("selectedIndex", 0)
  })

  const notifySound = new Audio("https://res.cloudinary.com/dxfq3iotg/video/upload/v1557233524/success.mp3");
  var row;
  var bodyFormData = new FormData()
  // On Edit
  $('.data-list-view').on("click", function (e) {
    console.log(e.target)

    row = e.target.parentNode.parentNode.parentNode;
    console.log(row)

    $('#data-name').val(row.children[2].textContent);
    $('#data-tel').val(row.children[3].textContent);
    $('#data-price').val(row.children[7].textContent);
    $('#data-status').val(row.children[5].children[0].children[0].children[0].textContent);
    $(".add-new-data").addClass("show");
    $(".overlay-bg").addClass("show");

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
  var sendOrderStatus = function (bodyFormData) {
    axios({
        method: 'post',
        url: '/edit_order_status',
        data: bodyFormData,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
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
  let notify = document.querySelector('.notify');
  let notifyIn = document.querySelector('.notifyIn');
  // mac chrome checkbox fix
  if (navigator.userAgent.indexOf("Mac OS X") != -1) {
    $(".dt-checkboxes-cell input, .dt-checkboxes").addClass("mac-checkbox")
  };
  $('.clear-notify').on('click', function () {
    notify.textContent = '';
    notifyIn.textContent = 0;
  });
  
  var noOfRepetitions = 7;

  notifySound.addEventListener('ended', function() {
            noOfRepetitions = noOfRepetitions-1;
            if (noOfRepetitions > 0) {
                this.currentTime = 0;
                this.play()};
}, false);

  const increaseNotfication = function () {
    if (notify.textContent === '') {
      notify.textContent = 1;
      notifyIn.textContent = 1;
    } else {
      notify.textContent = parseInt(notify.textContent) +  1;
      notifyIn.textContent =parseInt(notifyIn.textContent) + 1;
    }
    notifySound.play();
  
  };
  const renderItem = function (obj) {
    console.log(obj[0])
    console.log(obj[0].time);
    console.log(obj[0].user);
    console.log(obj[0].number);
    let itemMarkup;
    itemMarkup = `<tr>
                                    <td class="product-time">${obj[0].time}</td>
                                    <td class="product-number">${obj[0].number}</td>
                                    <td class="product-name">${obj[0].user.name}</td>
                                    <td class="product-category">${obj[0].user.phone_number}</td>
                                    <td class="product-address">${obj[0].user.address}</</td>
                                    <td>
                                        <div class="chip chip-info">
                                            <div class="chip-body">
                                                <div class="chip-text">${obj[0].status}</</div>
                                            </div>
                                        </div>
                                    </td>
                                    <td class="product-price">${obj[0].items}</td>
                                    <td class="product-price">{${obj[0].total} EGP</td>
                                    <td class="product-action">
                                        <span class="action-edit"><i class="feather icon-edit"></i></span>
                                    
                                    </td>
                                </tr>`

    return itemMarkup

  };
  const addItemTable = function (obj) {
    let item = renderItem(obj);
    document.querySelector('tbody').insertAdjacentHTML('afterbegin', item);
  }


  const socket = io();

  socket.on('connect', function () {
    socket.emit('message', {
      data: 'User Connected'
    });
    socket.on('order', function (order) {
      let item = JSON.parse(order);
      addItemTable(item);
      increaseNotfication();
    })
  });

})