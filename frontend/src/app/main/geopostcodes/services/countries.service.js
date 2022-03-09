(function () {
    'use strict';

    angular
        .module('app.geopostcodes')
        .factory('countriesService', countriesService);

    /** @ngInject */
    function countriesService($q, api) {

        var service = {
            countries: {
                data: [],
                count: 0,
                filters: {}
            },
            getCountries: getCountries
        };

        return service;

        //////////

        /**
         * Obtiene el listado de countries
         */
        function getCountries() {
            // Create a new deferred object
            var deferred = $q.defer();
            api.countries.get({page_size:"all"}, getOK, getKO);
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
