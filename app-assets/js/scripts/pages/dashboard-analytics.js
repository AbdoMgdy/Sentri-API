/*=========================================================================================
    File Name: dashboard-analytics.js
    Description: dashboard analytics page content with Apexchart Examples
==========================================================================================*/

$(window).on("load", function () {

  var $primary = '#7367F0';
  var $success = '#28c76f';
  var $danger = '#EA5455';
  var $warning = '#FF9F43';
  var $info = '#0DCCE1';
  var $primary_light = '#8F80F9';
  var $warning_light = '#FFC085';
  var $danger_light = '#f29292';
  var $info_light = '#1edec5';
  var $success_light = '#2ef06b';
  var $strok_color = '#b9c3cd';
  var $label_color = '#e7eef7';
  var $white = '#fff';
  var $delivered = parseInt(document.querySelector('.orders_delivered').textContent);
  var $out = parseInt(document.querySelector('.orders_out').textContent);
  var $pending = parseInt(document.querySelector('.orders_pending').textContent);
  var $canceled = parseInt(document.querySelector('.orders_canceled').textContent);
  var $total = $delivered + $pending + $canceled + $out;


  // Subscribers Gained Chart starts //
  // ----------------------------------

  var gainedChartoptions = {
    chart: {
      height: 250,
      type: 'area',
      toolbar: {
        show: false,
      },
      sparkline: {
        enabled: true
      },
      grid: {
        show: false,
        padding: {
          left: 0,
          right: 0
        }
      },
    },
    colors: [$primary],
    dataLabels: {
      enabled: false
    },
    stroke: {
      curve: 'smooth',
      width: 2.5
    },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 0.9,
        opacityFrom: 0.7,
        opacityTo: 0.5,
        stops: [0, 80, 100]
      }
    },
    series: [{
      name: 'Subscribers',
      data: [28, 40, 36, 52, 38, 60, 55]
    }],

    xaxis: {
      labels: {
        show: false,
      },
      axisBorder: {
        show: false,
      }
    },
    yaxis: [{
      y: 0,
      offsetX: 0,
      offsetY: 0,
      padding: { left: 0, right: 0 },
    }],
    tooltip: {
      x: { show: false }
    },
  }

  var gainedChart = new ApexCharts(
    document.querySelector("#subscribe-gain-chart"),
    gainedChartoptions
  );

  gainedChart.render();

  // Subscribers Gained Chart ends //



  // Orders Received Chart starts //
  // ----------------------------------

  var orderChartoptions = {
    chart: {
      height: 250,
      type: 'area',
      toolbar: {
        show: false,
      },
      sparkline: {
        enabled: true
      },
      grid: {
        show: false,
        padding: {
          left: 0,
          right: 0
        }
      },
    },
    colors: [$warning],
    dataLabels: {
      enabled: false
    },
    stroke: {
      curve: 'smooth',
      width: 2.5
    },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 0.9,
        opacityFrom: 0.7,
        opacityTo: 0.5,
        stops: [0, 80, 100]
      }
    },
    series: [{
      name: 'Orders',
      data: [10, 15, 8, 15, 7, 12, 8]
    }],

    xaxis: {
      labels: {
        show: false,
      },
      axisBorder: {
        show: false,
      }
    },
    yaxis: [{
      y: 0,
      offsetX: 0,
      offsetY: 0,
      padding: { left: 0, right: 0 },
    }],
    tooltip: {
      x: { show: false }
    },
  }

  var orderChart = new ApexCharts(
    document.querySelector("#orders-received-chart"),
    orderChartoptions
  );

  orderChart.render();

  // Orders Received Chart ends //

  
  // Product Order Chart starts
  // -----------------------------

  var productChartoptions = {
    chart: {
      height: 325,
      type: 'radialBar',
    },
    colors: [$success, $danger, $info , $warning],
    fill: {
      type: 'gradient',
      gradient: {
        enabled: true,
        shade: 'dark',
        type: 'vertical',
        shadeIntensity: 0.5,
        gradientToColors: [$success_light, $danger_light, $info_light, $warning_light],
        inverseColors: false,
        opacityFrom: 1,
        opacityTo: 1,
        stops: [25, 75]
      },
    },
    stroke: {
      lineCap: 'round'
    },
    plotOptions: {
      radialBar: {
        size: 165,
        hollow: {
          size: '30%'
        },
        track: {
          strokeWidth: '80%',
          margin: 15,
        },
        dataLabels: {
          name: {
            fontSize: '18px',
          },
          value: {
            fontSize: '16px',
          },
          total: {
            show: true,
            label: 'Total',

            formatter: function (w) {
              // By default this function returns the average of all series. The below is just an example to show the use of custom formatter function
              return $total // total orders
            }
          }
        }
      }
    },
    series: [Math.round(($delivered / $total) * 100), Math.round(($canceled / $total) * 100), Math.round(($pending / $total) * 100), Math.round(($out / $total) * 100)], // order status varibables
    labels: ['Delivered', 'Out', 'Pending', 'Canceled'],

  }



  var productChart = new ApexCharts(
    document.querySelector("#product-order-chart"),
    productChartoptions
  );

  productChart.render();

  // Product Order Chart ends //


  // Sales Chart starts
  // -----------------------------

  var salesChartoptions = {
    chart: {
      height: 400,
      type: 'radar',
      dropShadow: {
        enabled: true,
        blur: 8,
        left: 1,
        top: 1,
        opacity: 0.2
      },
      toolbar: {
        show: false
      },
    },
    toolbar: { show: false },
    series: [{
      name: 'Sales',
      data: [90, 50, 86, 40, 100, 20],
    }, {
      name: 'Visit',
      data: [70, 75, 70, 76, 20, 85],
    }],
    stroke: {
      width: 0
    },
    colors: [$primary, $info],
    plotOptions: {
      radar: {
        polygons: {
          strokeColors: ['#e8e8e8', 'transparent', 'transparent', 'transparent', 'transparent', 'transparent'],
          connectorColors: 'transparent'
        }
      }
    },
    fill: {
      type: 'gradient',
      gradient: {
        shade: 'dark',
        gradientToColors: ['#9f8ed7', $info_light],
        shadeIntensity: 1,
        type: 'horizontal',
        opacityFrom: 1,
        opacityTo: 1,
        stops: [0, 100, 100, 100]
      },
    },
    markers: {
      size: 0,
    },
    legend: {
      show: true,
      position: 'top',
      horizontalAlign: 'left',
      fontSize: '16px',
      markers: {
        width: 10,
        height: 10,
      }
    },
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    dataLabels: {
      style: {
        colors: [$strok_color, $strok_color, $strok_color, $strok_color, $strok_color, $strok_color]
      }
    },
    yaxis: {
      show: false,
    },
    grid: {
      show: false,
    },

  }

  var salesChart = new ApexCharts(
    document.querySelector("#sales-chart"),
    salesChartoptions
  );

  salesChart.render();

  // Sales Chart ends //

  /***** TOUR ******/
  var tour = new Shepherd.Tour({
    classes: 'shadow-md bg-purple-dark',
    scrollTo: true
  })

  // tour steps
  tour.addStep('step-1', {
    text: 'Toggle Collapse Sidebar.',
    attachTo: '.modern-nav-toggle .collapse-toggle-icon bottom',
    buttons: [

      {
        text: "Skip",
        action: tour.complete
      },
      {
        text: 'Next',
        action: tour.next
      },
    ]
  });

  tour.addStep('step-2', {
    text: 'Create your own bookmarks. You can also re-arrange them using drag & drop.',
    attachTo: '.bookmark-icons .icon-mail bottom',
    buttons: [

      {
        text: "Skip",
        action: tour.complete
      },

      {
        text: "previous",
        action: tour.back
      },
      {
        text: 'Next',
        action: tour.next
      },
    ]
  });

  tour.addStep('step-3', {
    text: 'You can change language from here.',
    attachTo: '.dropdown-language .flag-icon bottom',
    buttons: [

      {
        text: "Skip",
        action: tour.complete
      },

      {
        text: "previous",
        action: tour.back
      },
      {
        text: 'Next',
        action: tour.next
      },
    ]
  });

  tour.addStep('step-4', {
    text: 'Try fuzzy search to visit pages in flash.',
    attachTo: '.nav-link-search .icon-search bottom',
    buttons: [

      {
        text: "Skip",
        action: tour.complete
      },

      {
        text: "previous",
        action: tour.back
      },
      {
        text: 'Next',
        action: tour.next
      },
    ]
  });

  tour.addStep('step-5', {
    text: 'Buy this awesomeness at affordable price!',
    attachTo: '.buy-now bottom',
    buttons: [

      {
        text: "previous",
        action: tour.back
      },

      {
        text: "Finish",
        action: tour.complete
      },
    ]
  });

  if ($(window).width() > 1200 && !$("body").hasClass("menu-collapsed")) {
    tour.start()
  }
  else {
    tour.cancel()
  }
  if($("body").hasClass("horizontal-menu")){
    tour.cancel()
  }
  $(window).on("resize", function () {
    tour.cancel()
  })

});
