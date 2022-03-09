(function () {
    'use strict';

    angular
        .module('app.services')
        .factory('gasTypesService', gasTypesService);

    /** @ngInject */
    function gasTypesService($q, api) {

        var service = {
            gasTypes: {
                data: [],
                count: 0,
                filters: {}
            },
            getGasTypes: getGasTypes,
            getAllGasTypes: getAllGasTypes,
            getGasType: getGasType,
            saveGasType: saveGasType,
            getEmptyGasType: getEmptyGasType,
            removeGasType: removeGasType
        };

        return service;

        //////////

        /**
         * Obtiene el listado de gasTypes
         */
        function getGasTypes() {
            // Create a new deferred object
            var deferred = $q.defer();

            api.gasTypes.get(service.gasTypes.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                service.gasTypes.data=response.results;
                service.gasTypes.count = response.count;

                deferred.resolve(service.gasTypes);
            }

            function getKO(response) {
                //con esto evitamos que den problemas los not found cuando
                // filtramos y estamos en una página que ya no existe
                if(response.status==404 && service.gasTypes.filters.page!=1){
                    service.gasTypes.filters.page=1;
                    getGasTypes();
                }
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de gasTypes filtrando unicamente por el texto dado y sin guardar en el servicio
         *
         * @param search
         */
        function getAllGasTypes(search) {
            // Create a new deferred object
            var deferred = $q.defer();
            var f=angular.copy(service.gasTypes.filters);
            f.search=search;
            f.page_size="all";
            api.gasTypes.get(f, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene los datos de una gasType determinado por su ID
         *
         * @param id
         */
        function getGasType(id) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.gasTypes.get({id: id}, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Guarda la gasType que se pasa como parámetro. Si ya existe actualiza el existente.
         *
         * @param form
         */
        function saveGasType(form) {
            var deferred = $q.defer();

            var gasType = angular.copy(form);

            api.gasTypes.update(gasType, updateOK, saveKO);

            return deferred.promise;

            function createOK(response) {
                // Store the clients
                service.gasTypes.data.push(response);
                service.gasTypes.count ++;
                deferred.resolve(response);
            }

            function updateOK(response) {
                // Actauliza el listado
                for (var i = 0; i < service.gasTypes.data.length; i++) {
                    if (service.gasTypes.data[i].id === response.id) {
                        service.gasTypes.data[i] = angular.copy(response);
                    }
                }
                deferred.resolve(response);
            }

            function saveKO(response) {
                deferred.reject(response);
            }

        }

        /**
         * Devuelve un gasTypeo vacío
         */
        function getEmptyGasType() {
            return {
            };
        }

        function removeGasType(gasType){
            var deferred = $q.defer();

            api.gasTypes.remove({id: gasType.id}, gasTypeRemoveOK, removeKO);

            // GasTypeo borrado correctamente
            function gasTypeRemoveOK(response){
                // Quitamos la gasType en los datos locales
                for (var i = 0; i < service.gasTypes.data.length; i++) {
                    if (service.gasTypes.data[i].id === gasType.id) {
                        service.gasTypes.data.splice(i,1);
                        service.gasTypes.count -= 1;
                        break;
                    }
                }
                deferred.resolve(response.data);
            }

            // Fallo al borrar centro
            function removeKO(response){
                deferred.reject(response);
            }

            return deferred.promise;
        }


    }

})();
