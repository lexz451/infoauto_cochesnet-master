(function () {
  'use strict';

  angular
    .module('app.metrics')
    .factory('metricsService', metricsService);

  /** @ngInject */
  function metricsService($q, api) {

    var service = {
      metrics: {
        loading: false,
        filters: {}
      },
      benchmark: {
        data: {}
      },
      servicelevel: {
        data: {}
      },
      voiceservice: {
        data: {}
      },
      digitalservice: {
        data: {}
      },
      getMetrics: getMetrics,
      getBenchmark: getBenchmark,
      getServicelevel: getServicelevel,
      getVoiceService: getVoiceService,
      getDigitalService: getDigitalService,
    };

    return service;

    //////////

    /**
     * Obtiene el listado de metrics
     */
    function getMetrics() {
      var deferred = $q.defer();
      service.metrics.loading=true;
      var all = $q.all([getBenchmark(), getServicelevel(), getVoiceService(), getDigitalService()]);
      all.then(getOK);

      return deferred.promise;

      function getOK() {
        service.metrics.loading=false;
        deferred.resolve(service.metrics);
      }
    }
    /**
     * Obtiene el listado de metrics
     */
    function getBenchmark() {
      // Create a new deferred object
      var deferred = $q.defer();

      var f = angular.copy(service.metrics.filters);

      f.user_id__in = f.user_data.map(function (e) {
        return e.id;
      }).toString();
      delete f.user_data;


      if(!f.useful){
        delete f.useful;
      }

      api.benchmark.get(f, getOK, getKO);

      return deferred.promise;

      function getOK(response) {
        service.benchmark.data = processDataBenchmark(response);
        deferred.resolve(service.benchmark);
      }

      function getKO(response) {
        deferred.reject(response);
      }
    }

    function processDataBenchmark(response){
      response.funnel.lead_util=response.funnel.lead_util||0;
      response.funnel.lead_recibido=response.funnel.lead_recibido||0;
      response.funnel.ganados=response.funnel.ganados||0;
      response.funnel.lead_util_percentage=(response.funnel.lead_util*100/response.funnel.lead_recibido).toFixed(2);
      response.funnel.ganados_percentage=(response.funnel.ganados*100/response.funnel.lead_recibido).toFixed(2);
      response.total_origins={
        abiertos:0,
        descartados:0,
        ganados:0
      }
      response.total_users={
        abiertos:0,
        descartados:0,
        ganados:0
      }

      response.origins.forEach(function (o) {
        o.abiertos_percentage = (o.abiertos*100/o.total).toFixed(2)
        o.descartados_percentage = (o.descartados*100/o.total).toFixed(2)
        o.ganados_percentage = (o.ganados*100/o.total).toFixed(2)

        response.total_origins.abiertos+=o.abiertos;
        response.total_origins.descartados+=o.descartados;
        response.total_origins.ganados+=o.ganados;
      });
      response.total_origins.abiertos_percentage=(response.total_origins.abiertos*100/response.funnel.lead_recibido).toFixed(2);
      response.total_origins.descartados_percentage=(response.total_origins.descartados*100/response.funnel.lead_recibido).toFixed(2);
      response.total_origins.ganados_percentage=(response.total_origins.ganados*100/response.funnel.lead_recibido).toFixed(2);

      response.users.forEach(function (u) {
        u.abiertos_percentage = (u.abiertos*100/u.total).toFixed(2)
        u.descartados_percentage = (u.descartados*100/u.total).toFixed(2)
        u.ganados_percentage = (u.ganados*100/u.total).toFixed(2)

        response.total_users.abiertos+=u.abiertos;
        response.total_users.descartados+=u.descartados;
        response.total_users.ganados+=u.ganados;
      });
      response.total_users.abiertos_percentage=(response.total_users.abiertos*100/response.funnel.lead_recibido).toFixed(2);
      response.total_users.descartados_percentage=(response.total_users.descartados*100/response.funnel.lead_recibido).toFixed(2);
      response.total_users.ganados_percentage=(response.total_users.ganados*100/response.funnel.lead_recibido).toFixed(2);

      return response;
    }

    /**
     * Obtiene el listado de metrics
     */
    function getServicelevel() {
      // Create a new deferred object
      var deferred = $q.defer();

      var f = angular.copy(service.metrics.filters);

      f.user_id__in = f.user_data.map(function (e) {
        return e.id
      }).toString();
      delete f.user_data;

      if(!f.useful){
        delete f.useful;
      }

      api.servicelevel.get(f, getOK, getKO);

      return deferred.promise;

      function getOK(response) {
        service.servicelevel.data = processDataServicelevel(response);
        deferred.resolve(service.servicelevel);
      }

      function getKO(response) {
        deferred.reject(response);
      }
    }

    function processDataServicelevel(response){
      for(var i in response.kpis){
        if(i!=='total'){
          var number = response.kpis[i];
          var percentage = (number*100/response.kpis.total).toFixed(2);
          var title = i.split("_").join(" ");
          if(title.indexOf("sin ")!==-1){
            title = "Leads "+title;
          }else{
            title = "Leads con "+title;
          }
          response.kpis[i]={
            number:number,
            percentage:percentage,
            title:title
          };
          if(i==='tareas_realizadas'){
            response.kpis[i].filters={
              tasks__realization_date_check:true,
              tasks__is_traking_task:false,
            };
          }
          if(i==='tareas_programadas'){
            response.kpis[i].filters={
              tasks__is_traking_task:false,
            };
          }
          if(i==='sin_tareas_programadas'){
            response.kpis[i].filters={
              without_pending_tasks:true
            };
          }
          if(i==='tareas_atrasadas'){
            response.kpis[i].filters={
              tasks__realization_date_check:false,
              tasks__planified_realization_date__lt:new Date().toISOString(),
              tasks__is_traking_task:false,
            };
          }
          if(i==='seguimientos_realizados'){
            response.kpis[i].filters={
              tasks__realization_date__isnull:false,
              tasks__is_traking_task:true,
            };
          }
          if(i==='seguimientos_programados'){
            response.kpis[i].filters={
              tasks__is_traking_task:true,
            };
          }
          if(i==='sin_seguimientos_programados'){
            response.kpis[i].filters={
              without_pending_trackings:true
            };
          }
          if(i==='seguimientos_atrasados'){
            response.kpis[i].filters={
              tasks__realization_date_check:false,
              tasks__planified_realization_date__lt:new Date().toISOString(),
              tasks__is_traking_task:true,
            };
          }

          if(response.kpis[i] && response.kpis[i].filters){
            response.kpis[i].filters.with_concession = true;
          }
        }
      }

      return response;
    }

    /**
     * Obtiene el listado de metrics
     */
    function getVoiceService() {
      // Create a new deferred object
      var deferred = $q.defer();

      var f = angular.copy(service.metrics.filters);

      f.user_id__in = f.user_data.map(function (e) {
        return e.id
      }).toString();
      delete f.user_data;

      if(!f.useful){
        delete f.useful;
      }

      api.voiceService.get(f, getOK, getKO);

      return deferred.promise;

      function getOK(response) {
        service.voiceservice.data = processDataVoiceService(response);
        deferred.resolve(service.voiceservice);
      }

      function getKO(response) {
        deferred.reject(response);
      }
    }

    function processDataVoiceService(response){
      var llamadas={};
      llamadas.labels=response.llamadas.map(function (llamada) {
        return llamada.hour;
      });
      llamadas.atendidas=response.llamadas.map(function (llamada) {
        return llamada.total-llamada.no_atendidas;
      });
      llamadas.no_atendidas=response.llamadas.map(function (llamada) {
        return llamada.no_atendidas;
      });
      response.llamadas=llamadas;

      response.no_atendidos.con_llamadas_percentage = (response.no_atendidos.con_llamadas*100/response.totales.no_atendidas).toFixed(2);
      response.no_atendidos.sin_llamadas_percentage = (response.no_atendidos.sin_llamadas*100/response.totales.no_atendidas).toFixed(2);

      response.asa.tiempo=secondsToString(response.asa.tiempo);
      response.asa.menos_una_hora_percentage=(response.asa.menos_una_hora*100/response.asa.total).toFixed(2);

      return response;
    }

    /**
     * Obtiene el listado de metrics
     */
    function getDigitalService() {
      // Create a new deferred object
      var deferred = $q.defer();

      var f = angular.copy(service.metrics.filters);

      f.user_id__in = f.user_data.map(function (e) {
        return e.id
      }).toString();
      delete f.user_data;

      if(!f.useful){
        delete f.useful;
      }

      api.digitalService.get(f, getOK, getKO);

      return deferred.promise;

      function getOK(response) {
        service.digitalservice.data = processDataDigitalService(response);
        deferred.resolve(service.digitalservice);
      }

      function getKO(response) {
        deferred.reject(response);
      }
    }

    function processDataDigitalService(response){
      response.con_telefono.con_llamadas_percentage = (response.con_telefono.con_llamadas*100/response.totales.total).toFixed(2);
      response.con_telefono.sin_llamadas_percentage = (response.con_telefono.sin_llamadas*100/response.totales.total).toFixed(2);

      response.asa.tiempo=secondsToString(response.asa.tiempo);
      response.asa.menos_una_hora_percentage=(response.asa.menos_una_hora*100/response.asa.total).toFixed(2);

      return response;
    }

    function secondsToString(seconds) {
      var hour = Math.floor(seconds / 3600);
      var minute = Math.floor((seconds / 60) % 60);
      var second = seconds % 60;
      second = second.toFixed(0);
      return {hour:hour, minute:minute, second: second};
    }



  }

})();
