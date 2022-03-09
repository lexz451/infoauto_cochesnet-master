(function () {
    'use strict';

    angular
        .module('app.dashboard')
        .factory('dashboardService', dashboardService);

    /** @ngInject */
    function dashboardService($q, api) {

        var service = {
            dashboards: {
                data: [],
                count: 0,
                filters: {}
            },
            getDashboards: getDashboards,
            getDashboard: getDashboard
        };

        return service;

        //////////

        /**
         * Obtiene el listado de usuarios
         */
        function getDashboards() {
            // Create a new deferred object
            var deferred = $q.defer();
            api.dashboards.get(service.dashboards.filters, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                // Store the dashboards
                service.dashboards.data = response.results;
                service.dashboards.count = response.count;

                deferred.resolve(service.dashboards);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene los datos de un usuario determinado por su ID
         *
         * @param id
         */
        function getDashboard(id) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.dashboards.get({id: id}, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response.data);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

    }

})();
