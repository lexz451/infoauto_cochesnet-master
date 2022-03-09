(function () {
    'use strict';

    angular
        .module('app.origins')
        .factory('originsService', originsService);

    /** @ngInject */
    function originsService($q, api, $http) {

        var service = {
            origins: {
                data: [],
                count: 0,
                filters: {}
            },
            getOrigins: getOrigins,
            getAllOrigins: getAllOrigins,
            getOrigin: getOrigin,
            saveOrigin: saveOrigin,
            getEmptyOrigin: getEmptyOrigin,
            removeOrigin: removeOrigin
        };

        return service;

        //////////

        /**
         * Obtiene el listado de origins
         */
        function getOrigins() {
            // Create a new deferred object
            var deferred = $q.defer();

            api.origins.get(service.origins.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                service.origins.data=response.results;
                service.origins.count = response.count;

                deferred.resolve(service.origins);
            }

            function getKO(response) {
                //con esto evitamos que den problemas los not found cuando
                // filtramos y estamos en una página que ya no existe
                if(response.status==404 && service.origins.filters.page!=1){
                    service.origins.filters.page=1;
                    getOrigins();
                }
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de origins filtrando unicamente por el texto dado y sin guardar en el servicio
         *
         * @param search
         */
        function getAllOrigins(search) {
            // Create a new deferred object
            var deferred = $q.defer();
            var f=angular.copy(service.origins.filters);
            f.search=search;
            f.page_size="all";
            api.origins.get(f, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene los datos de una origin determinado por su ID
         *
         * @param id
         */
        function getOrigin(id) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.origins.get({id: id}, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Guarda la origin que se pasa como parámetro. Si ya existe actualiza el existente.
         *
         * @param form
         */
        function saveOrigin(form) {
            var deferred = $q.defer();

            var origin = angular.copy(form);

            if(origin.icon && origin.icon.indexOf("http")!==-1){
                delete origin.icon;
            }

            delete origin.phone_set;
            delete origin.email_set;

            if(form.id){
                api.origins.update(origin, updateOK, saveKO);
            }else{
                api.origins.create(origin, createOK, saveKO);
            }

            return deferred.promise;

            function createOK(response) {
                // Store the clients
                service.origins.data.push(response);
                service.origins.count ++;
                deferred.resolve(response);
            }

            function updateOK(response) {
                // Actauliza el listado
                for (var i = 0; i < service.origins.data.length; i++) {
                    if (service.origins.data[i].id === response.id) {
                        service.origins.data[i] = angular.copy(response);
                    }
                }
                deferred.resolve(response);
            }

            function saveKO(response) {
                deferred.reject(response);
            }

        }

        /**
         * Devuelve un origino vacío
         */
        function getEmptyOrigin() {
            return {
            };
        }

        function removeOrigin(origin){
            var deferred = $q.defer();

            api.origins.remove({id: origin.id}, originRemoveOK, removeKO);

            // Origino borrado correctamente
            function originRemoveOK(response){
                // Quitamos la origin en los datos locales
                for (var i = 0; i < service.origins.data.length; i++) {
                    if (service.origins.data[i].id === origin.id) {
                        service.origins.data.splice(i,1);
                        service.origins.count -= 1;
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
