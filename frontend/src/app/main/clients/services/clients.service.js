(function () {
    'use strict';

    angular
        .module('app.clients')
        .factory('clientsService', clientsService);

    /** @ngInject */
    function clientsService($q, api) {

        var service = {
            clients: {
                data: [],
                count: 0,
                filters: {}
            },
            getClients: getClients,
            getBusinessActivity: getBusinessActivity,
            getSectors: getSectors,
            sendWhatsapp: sendWhatsapp
        };

        return service;

        //////////

        /**
         * Obtiene el listado de clients
         */
        function getClients(search) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.clients.get({phone__icontains:search,page_size:"all"}, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de clients
         */
        function sendWhatsapp(msg) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.whatsapp.create(msg, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de clients
         */
        function getSectors(search) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.sectors.get({search:search,page_size:"50"}, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de clients
         */
        function getBusinessActivity(sector, search) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.businessActivity.get({sector__id:sector,search:search,page_size:"50"}, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }



    }

})();
