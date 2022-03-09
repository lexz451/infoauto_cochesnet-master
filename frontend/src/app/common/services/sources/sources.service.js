(function () {
    'use strict';

    angular
        .module('app.services')
        .factory('sourcesService', sourcesService);

    /** @ngInject */
    function sourcesService($q, api) {

        var service = {
            sources: {
                data: [],
                count: 0,
                filters: {}
            },
            getSources: getSources,
            getAllSources: getAllSources,
            getSource: getSource,
            saveSource: saveSource,
            getEmptySource: getEmptySource,
            removeSource: removeSource
        };

        return service;

        //////////

        /**
         * Obtiene el listado de sources
         */
        function getSources() {
            // Create a new deferred object
            var deferred = $q.defer();

            api.sources.get(service.sources.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                service.sources.data=response.results;
                service.sources.count = response.count;

                deferred.resolve(service.sources);
            }

            function getKO(response) {
                //con esto evitamos que den problemas los not found cuando
                // filtramos y estamos en una página que ya no existe
                if(response.status==404 && service.sources.filters.page!=1){
                    service.sources.filters.page=1;
                    getSources();
                }
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de sources filtrando unicamente por el texto dado y sin guardar en el servicio
         *
         * @param search
         */
        function getAllSources(search) {
            // Create a new deferred object
            var deferred = $q.defer();
            var f=angular.copy(service.sources.filters);
            f.search=search;
            f.page_size="all";
            api.sources.get(f, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene los datos de una source determinado por su ID
         *
         * @param id
         */
        function getSource(id) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.sources.get({id: id}, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Guarda la source que se pasa como parámetro. Si ya existe actualiza el existente.
         *
         * @param form
         */
        function saveSource(form) {
            var deferred = $q.defer();

            var source = angular.copy(form);

            api.sources.update(source, updateOK, saveKO);

            return deferred.promise;

            function createOK(response) {
                // Store the clients
                service.sources.data.push(response);
                service.sources.count ++;
                deferred.resolve(response);
            }

            function updateOK(response) {
                // Actauliza el listado
                for (var i = 0; i < service.sources.data.length; i++) {
                    if (service.sources.data[i].id === response.id) {
                        service.sources.data[i] = angular.copy(response);
                    }
                }
                deferred.resolve(response);
            }

            function saveKO(response) {
                deferred.reject(response);
            }

        }

        /**
         * Devuelve un sourceo vacío
         */
        function getEmptySource() {
            return {
            };
        }

        function removeSource(source){
            var deferred = $q.defer();

            api.sources.remove({id: source.id}, sourceRemoveOK, removeKO);

            // Sourceo borrado correctamente
            function sourceRemoveOK(response){
                // Quitamos la source en los datos locales
                for (var i = 0; i < service.sources.data.length; i++) {
                    if (service.sources.data[i].id === source.id) {
                        service.sources.data.splice(i,1);
                        service.sources.count -= 1;
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
