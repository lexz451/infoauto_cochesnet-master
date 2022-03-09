(function () {
  'use strict';
  angular
    .module('app.metrics')
    .controller('MetricsController', MetricsController);

  /** @ngInject */
  function MetricsController($scope, currentUser, metricsService, Benchmark, DigitalService, Servicelevel, VoiceService,
                             Metrics, $rootScope, DebounceService, $q, $timeout, cacheFactory, usersService) {
    var vm = this;
    // Data
    vm.user = currentUser;
    vm.metrics = Metrics;
    vm.benchmark = Benchmark;
    vm.digitalService = DigitalService;
    vm.servicelevel = Servicelevel;
    vm.voiceService = VoiceService;

    vm.data_origins = 'numbers';
    vm.data_users = 'numbers';
    vm.colors = ['gris', 'violeta', 'verde'];

    vm.calendarModel = [];
    vm.calendarUiConfig = {
      calendar: {
        defaultView       : 'agendaWeek',
        locale            : 'es',
        lang              : 'es',
        viewRender        : function (view)
        {
          vm.calendarView = view;
          vm.calendar = vm.calendarView.calendar;
          vm.metrics.filters.created_start_date=view.intervalStart._d;
          vm.metrics.filters.created_end_date=view.intervalEnd._d;
        },
        views: {
          agendaDay: { // name of view
            titleFormat: 'dddd, DD [de] MMMM [de] YYYY'
          }
        }
      }
    };

    // Watchers
    $scope.$watch('vm.metrics.filters', DebounceService(metricsService.getMetrics, 300), true);

    // Methods
    vm.getChart=getChart;
    vm.getFullUserName=getFullUserName;
    vm.copySearch=copySearch;
    vm.getUsers=getUsers;
    vm.getColor = getColor;
    vm.concatFilters = concatFilters;

    //////////
    function getChart() {
      vm.donutChartDigital = {
        data   : {
          series: [vm.digitalService.data.con_telefono.con_llamadas, vm.digitalService.data.con_telefono.sin_llamadas]
        },
        options: {
          donut: true,
          height: '450px',
        },
        events : {
          draw: function (data)
          {
            if ( data.type === 'slice' )
            {
              var color=(data.index===0)? '#3182ce' : '#63b3ed'
              data.element.attr({
                style: 'stroke:'+color
              });
            }
          }
        }
      };

      vm.stackedBarChart = {
        data   : {
          labels: vm.voiceService.data.llamadas.labels,
          series: [
            vm.voiceService.data.llamadas.atendidas,
            vm.voiceService.data.llamadas.no_atendidas,
          ]
        },
        options: {
          stackBars: true,
          axisY    : {
            labelInterpolationFnc: function (value)
            {
              return value;
            }
          },
          height: '450px',
          plugins: [
            Chartist.plugins.tooltip()
          ]
        },
        events : {
          draw: function (data)
          {
            if ( data.type === 'bar' )
            {
              var color=(data.seriesIndex===0)? '#448aff' : '#e0e0e0'
              data.element.attr({
                style: 'stroke:'+color
              });
            }
          }
        }
      };

      vm.donutChart = {
        data   : {
          series: [vm.voiceService.data.no_atendidos.con_llamadas, vm.voiceService.data.no_atendidos.sin_llamadas]
        },
        options: {
          donut: true,
          height: '450px',
        },
        events : {
          draw: function (data)
          {
            if ( data.type === 'slice' )
            {
              var color=(data.index===0)? '#3182ce' : '#63b3ed'
              data.element.attr({
                style: 'stroke:'+color
              });
            }
          }
        }
      };
    }

    function getFullUserName(user) {
      return user.first_name + " " + user.last_name;
    }

    function copySearch(item) {
      var a = angular.copy(vm[item]);
      if(a){
        $timeout(function () {
          vm[item]=a;
        },100)
      }
    }

    /* Usuarios */
    function getUsers(searchText) {
      var deferred = $q.defer();
      var users = angular.copy(cacheFactory.usersService.get(searchText));
      if(!users){
        usersService.users.filters = {};
        usersService.users.filters.search = searchText;
        usersService.users.filters.page_size = "20";
        usersService.users.filters.is_complex = false;
        usersService.getUsers(searchText).then(function (users) {
          cacheFactory.usersService.put(searchText, users);
          deferred.resolve(excludeArr(users.data, vm.metrics.filters.user_data));
        });
      }else{
        deferred.resolve(excludeArr(users.data, vm.metrics.filters.user_data));
      }

      return deferred.promise;
    }

    function excludeArr(arr1, arr2, key) {
      if(!key){
        key='id';
      }
      for(var i=arr1.length-1; i >= 0; i--) {
        for(var j=arr2.length-1; j >= 0; j--) {
          if(arr1[i] && arr1[i][key] === arr2[j][key])
          {
            arr1.splice(i,1);
          }
        }
      }
      return arr1;
    }

    function getColor($index){
      var i=($index - (vm.colors.length*Math.trunc($index/vm.colors.length)));
      return vm.colors[i];
    }

    function concatFilters(o1, o2){
      var f=Object.assign({}, o1, o2);
      f.created_end_date=new Date(f.created_end_date).toISOString();
      f.created_start_date=new Date(f.created_start_date).toISOString();
      f.user_id__in = f.user_data.map(function (e) {
        return e.id;
      }).toString();
      return f;
    }


  }
})();
