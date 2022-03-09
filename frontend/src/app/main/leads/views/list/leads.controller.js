(function () {
  'use strict';
  angular
    .module('app.leads')
    .controller('LeadsController', LeadsController);

  /** @ngInject */
  function LeadsController($scope, currentUser, leadsService, Leads, Kpis, NotifyService, leadStatusService, $mdSidenav,
                           usersService, concessionairesService, originsService, channelsService, vehiclesService,
                           taskTypesService, mediaTypesService, eventsService, $q, $timeout, cacheFactory, leadResultsService,
                           $mdDialog, $rootScope, $document, DebounceService, $state, gettextCatalog, $stateParams) {
    var vm = this;
    // Data
    vm.user = currentUser;
    vm.leads = Leads;
    vm.kpis = Kpis;

    vm.results=leadResultsService.newLeadResults;
    vm.resultReasons=leadResultsService.resultReasons;

    vm.filters = {
      search: "",
      date_start: null,
      date_end: null,
      created_start_date: null,
      created_end_date: null,
      user_data: [vm.user],
      concessionaire__in_data: [],
      status_data: [],
      origin_data: [],
      channel_data: [],
      tasks_media_data: [],
      brand_data: [],
      tasks_type_data: [],
      tasks_tracing_data: []
    };

    if($stateParams.created_start_date) {
      vm.filters = Object.assign({}, $stateParams, vm.filters);
      vm.filters.created_start_date = parseISOString($stateParams.created_start_date);
      vm.filters.created_end_date = parseISOString($stateParams.created_end_date);
      vm.filters.user_data = [];
    }

    vm.leadStatus = leadStatusService.leadStatus;

    // Watchers
    $scope.$watch('vm.leads.filters', DebounceService(leadsService.getLeads, 300), true);
    $scope.$watch('vm.kpis.filters', DebounceService(eventsService.getKpis, 300), true);


    // Methods
    vm.goLead = goLead;
    vm.toggleKpi = toggleKpi;
    vm.changeOrder = changeOrder;
    vm.changeFilter = changeFilter;
    vm.toggleSidenav = toggleSidenav;
    vm.setScore = setScore;
    vm.getUsers = getUsers;
    vm.getFullUserName = getFullUserName;
    vm.getConcessionaires = getConcessionaires;
    vm.getOrigins = getOrigins;
    vm.getChannels = getChannels;
    vm.getTaskMedia = getTaskMedia;
    vm.getBrands = getBrands;
    vm.getTaskTypes = getTaskTypes;
    vm.getBooleans = getBooleans;
    vm.getRequestTypes = getRequestTypes;
    vm.getStatusLead = getStatusLead;
    vm.setFilters = setFilters;
    vm.copySearch = copySearch;
    vm.getDocument = getDocument;

    //////////
    function parseISOString(s) {
      if(s){
        var b = s.split(/\D+/);
        return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
      }
      return null;
    }

    function goLead(lead) {
      var url = $state.href('app.leads.get.edit', {lead: lead.id});
      window.open(url,'_blank');
    }

    /**
     * Activa/Desactiva el filtro del kpi
     *
     * @param item
     */
    function toggleKpi(item) {
      for (var kpi in vm.kpis.data) {
        for (var k in vm.kpis.data[kpi].kpis) {
          vm.kpis.data[kpi].kpis[k].active = false;
        }
      }
      if (vm.leads.filters.kpi_filter === item.filter_key) {
        item.active = false;
        vm.leads.filters.kpi_filter = null;
      } else {
        item.active = true;
        vm.leads.filters.kpi_filter = item.filter_key;
      }
    }
    /**
     * Ordena la tabla
     *
     * @param field
     */
    function changeOrder(field) {
      if(vm.leads.filters.ordering===field){
        vm.leads.filters.ordering='-'+field;
      }else{
        vm.leads.filters.ordering=field;
      }
    }



    /**
     * Toggle sidenav
     *
     * @param sidenavId
     */
    function toggleSidenav(sidenavId) {
      $mdSidenav(sidenavId).toggle();
    }

    //FILTERS SIDENAV

    /**
     * Change filters
     *
     * @param key
     * @param value
     */
    function changeFilter(key, value) {
      minDateFilter();
      maxDateFilter();

      if (key === 'last_action_end_date') {
        value.setHours(23, 59, 59, 999);
      }

      vm.filters[key] = value;
      vm.leads.filters.page = 1;
      vm.leads.filters[key] = value;

    }

    function minDateFilter() {
      if (vm.filters.date_end) {
        vm.minDate = moment(vm.filters.date_end).subtract(30, 'd').toDate();
      } else {
        vm.minDate = null;
      }

    }

    function maxDateFilter() {
      if (vm.filters.date_start) {
        vm.maxDate = moment(vm.filters.date_start).add(30, 'd').toDate();
      } else {
        vm.maxDate = null;
      }
    }

    function setScore(score) {
      if (vm.filters.score === score) {
        vm.filters.score = null;
      } else {
        vm.filters.score = score;
      }
      //vm.changeFilter('score', vm.filters.score)
    }

    /* Usuarios */
    function getUsers(searchText) {
      var deferred = $q.defer();
      var users = angular.copy(cacheFactory.usersService.get(searchText));
      if(!users){
        usersService.users.filters = {};
        usersService.users.filters.search = searchText;
        usersService.users.filters.page_size = "50";
        usersService.users.filters.is_complex = false;
        usersService.getUsers(searchText).then(function (users) {
          cacheFactory.usersService.put(searchText, users);
          deferred.resolve(excludeArr(users.data, vm.filters.user_data));
        });
      }else{
        deferred.resolve(excludeArr(users.data, vm.filters.user_data));
      }

      return deferred.promise;
    }

    function getFullUserName(user) {
      return user.first_name + " " + user.last_name;
    }

    /* Concesionarios */
    function getConcessionaires(searchText) {
      var deferred = $q.defer();
      var concessionaires = angular.copy(cacheFactory.concessionairesService.get(searchText));
      if(!concessionaires){
        concessionairesService.concessionaires.filters = {};
        concessionairesService.concessionaires.filters.search = searchText;
        concessionairesService.concessionaires.filters.page_size = "50";
        concessionairesService.concessionaires.filters.is_complex = false;
        concessionairesService.getConcessionaires().then(function (concessionaires) {
          cacheFactory.concessionairesService.put(searchText, concessionaires);
          deferred.resolve(excludeArr(concessionaires.data, vm.filters.concessionaire__in_data));
        });
      }else{
        deferred.resolve(excludeArr(concessionaires.data, vm.filters.concessionaire__in_data));
      }

      return deferred.promise;
    }

    /* Orígenes */
    function getOrigins(searchText) {
      var deferred = $q.defer();
      var origins = angular.copy(cacheFactory.originsService.get(searchText));
      if(!origins){
        originsService.getAllOrigins(searchText).then(function (origins) {
          cacheFactory.originsService.put(searchText, origins);
          deferred.resolve(excludeArr(origins,vm.filters.origin_data));
        });
      }else{
        deferred.resolve(excludeArr(origins, vm.filters.origin_data));
      }

      return deferred.promise;
    }

    /* Canales */
    function getChannels(searchText) {
      var deferred = $q.defer();
      var channels = angular.copy(cacheFactory.channelsService.get(searchText));
      if(!channels){
        channelsService.getAllChannels(searchText).then(function (channels) {
          cacheFactory.channelsService.put(searchText, channels);
          deferred.resolve(excludeArr(channels,vm.filters.channel_data));
        });
      }else{
        deferred.resolve(excludeArr(channels, vm.filters.channel_data));
      }

      return deferred.promise;
    }

    /* Task Media */
    function getTaskMedia(searchText) {
      var deferred = $q.defer();

      var t = [
        {id: "Whatsapp", name: "Whatsapp"},
        {id: "Phone", name: "Teléfono"},
        {id: "SMS", name: "SMS"},
        {id: "E-mail", name: "Email"},
        {id: "face", name: "Presencial"}
      ]
      deferred.resolve(excludeArr(t,vm.filters.tasks_media_data));

      return deferred.promise;
    }

    /* Marcas */
    function getBrands(searchText) {
      var deferred = $q.defer();
      var brands = angular.copy(cacheFactory.vehiclesService.get(searchText));
      if(!brands){
        vehiclesService.getBrands(searchText).then(function (brands) {
          cacheFactory.vehiclesService.put(searchText, brands);
          deferred.resolve(excludeArr(brands,vm.filters.brand_data));
        });
      }else{
        deferred.resolve(excludeArr(brands, vm.filters.brand_data));
      }

      return deferred.promise;
    }

    /* Task types */
    function getTaskTypes(tracing, searchText) {
      var deferred = $q.defer();
      var res = angular.copy(cacheFactory.taskTypesService.get(searchText+tracing));
      if(!res){
        taskTypesService.getTaskTypes(tracing).then(function (res) {
          cacheFactory.taskTypesService.put(searchText+tracing, res);
          if(tracing){
            deferred.resolve(excludeArr(res,vm.filters.tasks_tracing_data, 'key'));
          }else{
            deferred.resolve(excludeArr(res,vm.filters.tasks_type_data, 'key'));
          }
        });
      }else{
        if(tracing){
          deferred.resolve(excludeArr(res,vm.filters.tasks_tracing_data, 'key'));
        }else{
          deferred.resolve(excludeArr(res,vm.filters.tasks_type_data, 'key'));
        }
      }

      return deferred.promise;
    }

    /* boolean select */
    function getBooleans() {
      var deferred = $q.defer();

      var b = [
        {id: true, name: "Vencida"},
        {id: false, name: "No vencida"}
      ]
      deferred.resolve(b);

      return deferred.promise;
    }

    /* Request type */
    function getRequestTypes() {
      var deferred = $q.defer();

      var t= [
        {id: 'tarea', name: gettextCatalog.getString('Tarea')},
        {id: 'seguimiento', name: gettextCatalog.getString('Seguimiento')},
      ]
      deferred.resolve(t);

      return deferred.promise;
    }

    /* Status lead */
    function getStatusLead() {
      var deferred = $q.defer();

      var status= [
        {id: 'new', name: gettextCatalog.getString('Leads no atendidos')},
        {id: 'attended', name: gettextCatalog.getString('Leads atendidos')},
        {id: 'commercial_management', name: gettextCatalog.getString('Tareas pendientes')},
        {id: 'tracing', name: gettextCatalog.getString('Seguimiento')},
        {id: 'end', name: gettextCatalog.getString('Leads cerrados')}
      ]
      deferred.resolve(excludeArr(status,vm.filters.status_data));

      return deferred.promise;
    }

    function setFilters() {
      //kpis
      //vm.kpis.filters.start=moment(vm.filters.date_start).format("YYYY-MM-DD");
      //vm.kpis.filters.end=moment(vm.filters.date_end).add(1,'d').format("YYYY-MM-DD");

      //leads
      var tasks_type_data = vm.filters.tasks_type_data.map(function (e) {
        return e.key;
      }).toString();
      var tasks_tracing_data = vm.filters.tasks_tracing_data.map(function (e) {
        return e.key;
      }).toString();
      if (tasks_type_data !== "" && tasks_tracing_data !== "") {
        tasks_type_data += ",";
      }
      tasks_type_data += tasks_tracing_data;

      var f = {
        with_concession: vm.filters.with_concession,
        search: vm.filters.search,
        score: vm.filters.score,
        date_start: vm.filters.date_start,
        date_end: vm.filters.date_end,
        created_start_date: vm.filters.created_start_date,
        created_end_date: vm.filters.created_end_date,
        result:vm.filters.result,
        result_reason:vm.filters.result_reason,
        status__in:vm.filters.status_data.map(function (e) { return e.id }).toString(),
        user_id__in: vm.filters.user_id__in,
        concessionaire__in: vm.filters.concessionaire__in_data.map(function (e) {
          return e.id
        }).toString(),
        source__origin_id__in: vm.filters.origin_data.map(function (e) {
          return e.id
        }).toString(),
        source__channel_id__in: vm.filters.channel_data.map(function (e) {
          return e.id
        }).toString(),
        tasks__media__in: vm.filters.tasks_media_data.map(function (e) {
          return e.id
        }).toString(),
        vehicles__brand_model__in: vm.filters.brand_data.map(function (e) {
          return e.name + "," + e.name + "___" + e.id
        }).toString(),
        vehicles__model__icontains: vm.filters.model,
        vehicles__version__icontains: vm.filters.version,
        tasks__type__in: tasks_type_data,
      };

      if (vm.filters.user_data.length > 0) {
        f.user_id__in = vm.filters.user_data.map(function (e) {
          return e.id;
        }).toString();
      }

      if (vm.filters.overdue) {
        //Tarea vencida
        if (vm.filters.overdue && vm.filters.overdue.id) {
          f.tasks__planified_realization_date__lt = moment().format();
          f.tasks__planified_realization_date__gt = null;
        } else { //Tarea no vencida
          f.tasks__planified_realization_date__gt = moment().format();
          f.tasks__planified_realization_date__lt = null;
        }
        f.tasks__realization_date_check = false;
        f.tasks__tracking_date_check = false;
      } else {
        f.tasks__planified_realization_date__lt = null;
        f.tasks__planified_realization_date__gt = null;
        f.tasks__realization_date_check = null;
        f.tasks__tracking_date_check = null;
      }

      for (var i in f) {
        changeFilter(i, f[i]);
      }
    }

    function copySearch(item) {
      var a = angular.copy(vm[item]);
      if(a){
        $timeout(function () {
          vm[item]=a;
        },100)
      }
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

    function getDocument() {
      setFilters();
      var f = angular.copy(vm.leads.filters);
      return concessionairesService.getDocument(f).then(function (response) {
        downloadFile(response, "leads.xls", "leads.xls");
      }, function (error) {
        NotifyService.errorMessage(gettextCatalog.getString("Error al exportar leads"));
      });
    }

    //Descarga cualquier tipo de fichero
    function downloadFile(response, name, type) {
      var blob = new Blob([response], {type: type});

      if (window.navigator && window.navigator.msSaveOrOpenBlob) {
        window.navigator.msSaveOrOpenBlob(blob);
      } else {
        var link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = name;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
    }

  }
})();
