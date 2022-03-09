(function () {
    'use strict';

    angular
        .module('app.services')
        .factory('phonesService', phonesService);

    /** @ngInject */
    function phonesService($q, api) {

        var service = {
            phones: {
                data: [],
                count: 0,
                filters: {}
            },
            getPhones: getPhones,
            getAllPhones: getAllPhones,
            getPhone: getPhone,
            savePhone: savePhone,
            getEmptyPhone: getEmptyPhone,
            removePhone: removePhone
        };

        return service;

        //////////

        /**
         * Obtiene el listado de phones
         */
        function getPhones() {
            // Create a new deferred object
            var deferred = $q.defer();

            api.phones.get(service.phones.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                service.phones.data=response.results;
                service.phones.count = response.count;

                deferred.resolve(service.phones);
            }

            function getKO(response) {
                //con esto evitamos que den problemas los not found cuando
                // filtramos y estamos en una página que ya no existe
                if(response.status==404 && service.phones.filters.page!=1){
                    service.phones.filters.page=1;
                    getPhones();
                }
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de phones filtrando unicamente por el texto dado y sin guardar en el servicio
         *
         * @param search
         */
        function getAllPhones(search) {
            // Create a new deferred object
            var deferred = $q.defer();
            var f=angular.copy(service.phones.filters);
            f.search=search;
            f.page_size="all";
            api.phones.get(f, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene los datos de una phone determinado por su ID
         *
         * @param id
         */
        function getPhone(id) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.phones.get({id: id}, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Guarda la phone que se pasa como parámetro. Si ya existe actualiza el existente.
         *
         * @param form
         */
        function savePhone(form) {
            var deferred = $q.defer();

            var phone = angular.copy(form);

            api.phones.update(phone, updateOK, saveKO);

            return deferred.promise;

            function createOK(response) {
                // Store the clients
                service.phones.data.push(response);
                service.phones.count ++;
                deferred.resolve(response);
            }

            function updateOK(response) {
                // Actauliza el listado
                for (var i = 0; i < service.phones.data.length; i++) {
                    if (service.phones.data[i].id === response.id) {
                        service.phones.data[i] = angular.copy(response);
                    }
                }
                deferred.resolve(response);
            }

            function saveKO(response) {
                deferred.reject(response);
            }

        }

        /**
         * Devuelve un phoneo vacío
         */
        function getEmptyPhone() {
            return {
            };
        }

        function removePhone(phone){
            var deferred = $q.defer();

            api.phones.remove({id: phone.id}, phoneRemoveOK, removeKO);

            // Phoneo borrado correctamente
            function phoneRemoveOK(response){
                // Quitamos la phone en los datos locales
                for (var i = 0; i < service.phones.data.length; i++) {
                    if (service.phones.data[i].id === phone.id) {
                        service.phones.data.splice(i,1);
                        service.phones.count -= 1;
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
