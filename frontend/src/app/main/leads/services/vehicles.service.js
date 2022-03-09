(function () {
    'use strict';

    angular
        .module('app.leads')
        .factory('vehiclesService', vehiclesService);

    /** @ngInject */
    function vehiclesService($q, api) {

        var service = {
            removeVehicle: removeVehicle,
            getBrands: getBrands,
            getModels: getModels,
            getVersions: getVersions
        };

        return service;

        //////////
        
        function removeVehicle(vehicle){
            var deferred = $q.defer();

            api.vehicles.remove({id: vehicle.id}, vehicleRemoveOK, removeKO);

            // Vehicle borrado correctamente
            function vehicleRemoveOK(response){
                deferred.resolve(response.data);
            }

            // Fallo al borrar vehicle
            function removeKO(response){
                deferred.reject(response);
            }

            return deferred.promise;
        }

        /**
         * Obtiene el listado de brands
         */
        function getBrands(search) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.brands.get({search:search,page_size:"all"}, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                if(search && response.count<1){
                    response.results.push({id:null,name:search})
                }
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de modelos
         */
        function getModels(brand, search) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.models.get({brand__id:brand, search:search ,page_size:"50"}, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                if(search && response.count<1){
                    response.results.push({id:null,model_name:search})
                }
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de versiones
         */
        function getVersions(model, search) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.versions.get({vehicle_model__id:model, search:search ,page_size:"50"}, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                if(search && response.count<1){
                    response.results.push({id:null,version_name:search})
                }
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

    }


})();
