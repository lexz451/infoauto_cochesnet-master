(function () {
    'use strict';

    angular
        .module('app.geopostcodes')
        .factory('provincesService', provincesService);

    /** @ngInject */
    function provincesService($q, api) {

        var service = {
            provinces: {
                data: [],
                count: 0,
                filters: {}
            },
            getProvinces: getProvinces
        };

        return service;

        //////////

        /**
         * Obtiene el listado de provinces
         */
        function getProvinces(country,search) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.provinces.get({country:country,page_size:"all"}, getOK, getKO);
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
