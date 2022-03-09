(function () {
    'use strict';

    angular
        .module('app.calendar')
        .factory('eventsService', eventsService);

    /** @ngInject */
    function eventsService($q, api, localStorageService) {

        var service = {
            leads: {
                filters: {}
            },
            kpis: {
                data: [],
                count: 0,
                filters: {}
            },
            kpisPositive: {
                data: [],
                count: 0,
                filters: {}
            },
            getEvents: getEvents,
            getKpis:getKpis,
            reloadKpis:reloadKpis,
            getKpisPositive:getKpisPositive,
            reloadKpisPositive:reloadKpisPositive,
        };

        return service;

        //////////

        /**
         * Obtiene el listado de citas
         */
        function getUrl() {
            return api.URLs.calendar;
        }
        /**
         * Obtiene el listado de citas
         */
        function getEvents() {
            return [{
                url: getUrl(),
                beforeSend : function (request, data) {
                    var urlParams = new URLSearchParams(data.url.split('?')[1]);

                    var f=angular.copy(service.leads.filters);

                    if(f.user_data && f.user_data.id){
                        f.user=f.user_data.id;
                    }
                    delete f.user_data;

                    service.kpis.filters.start=urlParams.get('start');
                    service.kpis.filters.end=urlParams.get('end');
                    service.kpis.filters.user=f.user;

                    service.kpisPositive.filters.start=urlParams.get('start');
                    service.kpisPositive.filters.end=urlParams.get('end');
                    service.kpisPositive.filters.user=f.user;

                    var str = "";
                    for (var key in f) {
                        if(f[key]!==null){
                            str += "&";
                            str += key + "=" + encodeURIComponent(f[key]);
                        }
                    }
                    data.url+=str;
                    if(localStorageService.get('token')){
                        request.setRequestHeader("Authorization", 'Token ' + localStorageService.get('token'));
                    }
                }
            }]
        }

        /**
         * Obtiene el listado de kpis
         */
        function getKpis() {
            // Create a new deferred object
            var deferred = $q.defer();

            api.leads.kpis(service.kpis.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                service.kpis.data = response.kpis;
                service.kpis.count = response.kpis.length;

                deferred.resolve(service.kpis);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Actualiza el listado de kpis
         */
        function reloadKpis() {
            // Create a new deferred object
            var deferred = $q.defer();

            api.leads.kpis(service.kpis.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
              if(service.kpis.data.length>0){
                for(var i in service.kpis.data){
                  for(var j in response.kpis) {
                    if(service.kpis.data[i].name===response.kpis[j].name){
                      service.kpis.data[i].kpis = response.kpis[j].kpis;
                    }
                  }
                }
              }else{
                service.kpis.data = response.kpis;
                service.kpis.count = response.kpis.length;
              }
              deferred.resolve(service.kpis);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de kpis ganados
         */
        function getKpisPositive() {
            // Create a new deferred object
            var deferred = $q.defer();

            api.leads.kpis(service.kpisPositive.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                service.kpisPositive.data = response.kpis;
                service.kpisPositive.count = response.kpis.length;

                deferred.resolve(service.kpisPositive);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

      /**
       * Actualiza el listado de kpis ganados
       */
      function reloadKpisPositive() {
        // Create a new deferred object
        var deferred = $q.defer();

        api.leads.kpis(service.kpisPositive.filters, getOK, getKO);

        return deferred.promise;

        function getOK(response) {
          if(service.kpisPositive.data.length>0){
            for(var i in service.kpisPositive.data){
              for(var j in response.kpis) {
                if(service.kpisPositive.data[i].name===response.kpis[j].name){
                  service.kpisPositive.data[i].kpis = response.kpis[j].kpis;
                }
              }
            }
          }else{
            service.kpisPositive.data = response.kpis;
            service.kpisPositive.count = response.kpis.length;
          }
          deferred.resolve(service.kpisPositive);
        }

        function getKO(response) {
          deferred.reject(response);
        }
      }

    }

})();
