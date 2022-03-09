(function () {
    'use strict';

    angular
        .module('app.geopostcodes')
        .factory('localitiesService', localitiesService);

    /** @ngInject */
    function localitiesService($q, api) {

        var service = {
            localities: {
                data: [],
                count: 0,
                filters: {}
            },
            getLocalities: getLocalities,
            getLocalitiesByCodPostal: getLocalitiesByCodPostal
        };

        return service;

        //////////

        /**
         * Obtiene el listado de localities
         */
        function getLocalities(province, search) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.localities.get({province:province, search:search ,page_size:"50"}, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }
        /**
         * Obtiene el listado de localities
         */
        function getLocalitiesByCodPostal(codPostal) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.localities.get({postal_code:codPostal ,page_size:"all"}, getOK, getKO);
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
