(function () {
    'use strict';

    angular
        .module('app.services')
        .factory('click2callsService', click2callsService);

    /** @ngInject */
    function click2callsService($q, leadsService, api) {

        var service = {
            click2calls: {
                data: [],
                count: 0,
                filters: {}
            },
            getClick2calls: getClick2calls,
            getAllClick2calls: getAllClick2calls,
            getClick2call: getClick2call,
            saveClick2call: saveClick2call,
            getEmptyClick2call: getEmptyClick2call,
            removeClick2call: removeClick2call
        };

        return service;

        //////////

        /**
         * Obtiene el listado de click2calls
         */
        function getClick2calls() {
            // Create a new deferred object
            var deferred = $q.defer();

            api.click2calls.get(service.click2calls.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                service.click2calls.data=response.results;
                service.click2calls.count = response.count;

                deferred.resolve(service.click2calls);
            }

            function getKO(response) {
                //con esto evitamos que den problemas los not found cuando
                // filtramos y estamos en una página que ya no existe
                if(response.status==404 && service.click2calls.filters.page!=1){
                    service.click2calls.filters.page=1;
                    getClick2calls();
                }
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de click2calls filtrando unicamente por el texto dado y sin guardar en el servicio
         *
         * @param search
         */
        function getAllClick2calls(search) {
            // Create a new deferred object
            var deferred = $q.defer();
            var f=angular.copy(service.click2calls.filters);
            f.search=search;
            f.page_size="all";
            api.click2calls.get(f, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene los datos de una click2call determinado por su ID
         *
         * @param id
         */
        function getClick2call(id) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.click2calls.get({id: id}, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Guarda la click2call que se pasa como parámetro. Si ya existe actualiza el existente.
         *
         * @param form
         */
        function saveClick2call(form) {
            var deferred = $q.defer();

            var click2call = angular.copy(form);

            api.click2calls.create(click2call, createOK, saveKO);

            return deferred.promise;

            function createOK(response) {
                leadsService.getLeadsOutgoingCalls(form.lead).then(function(){
                    deferred.resolve(response);
                });
            }

            function saveKO(response) {
                deferred.reject(response);
            }

        }

        /**
         * Devuelve un click2callo vacío
         */
        function getEmptyClick2call() {
            return {
            };
        }

        function removeClick2call(click2call){
            var deferred = $q.defer();

            api.click2calls.remove({id: click2call.id}, click2callRemoveOK, removeKO);

            // Click2callo borrado correctamente
            function click2callRemoveOK(response){
                // Quitamos la click2call en los datos locales
                for (var i = 0; i < service.click2calls.data.length; i++) {
                    if (service.click2calls.data[i].id === click2call.id) {
                        service.click2calls.data.splice(i,1);
                        service.click2calls.count -= 1;
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
