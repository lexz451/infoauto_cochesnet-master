(function () {
    'use strict';

    angular
        .module('app.services')
        .factory('emailsService', emailsService);

    /** @ngInject */
    function emailsService($q, api) {

        var service = {
            emails: {
                data: [],
                count: 0,
                filters: {}
            },
            getEmails: getEmails,
            getAllEmails: getAllEmails,
            getEmail: getEmail,
            saveEmail: saveEmail,
            getEmptyEmail: getEmptyEmail,
            removeEmail: removeEmail
        };

        return service;

        //////////

        /**
         * Obtiene el listado de emails
         */
        function getEmails() {
            // Create a new deferred object
            var deferred = $q.defer();

            api.emails.get(service.emails.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                service.emails.data=response.results;
                service.emails.count = response.count;

                deferred.resolve(service.emails);
            }

            function getKO(response) {
                //con esto evitamos que den problemas los not found cuando
                // filtramos y estamos en una página que ya no existe
                if(response.status==404 && service.emails.filters.page!=1){
                    service.emails.filters.page=1;
                    getEmails();
                }
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de emails filtrando unicamente por el texto dado y sin guardar en el servicio
         *
         * @param search
         */
        function getAllEmails(search) {
            // Create a new deferred object
            var deferred = $q.defer();
            var f=angular.copy(service.emails.filters);
            f.search=search;
            f.page_size="all";
            api.emails.get(f, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene los datos de una email determinado por su ID
         *
         * @param id
         */
        function getEmail(id) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.emails.get({id: id}, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Guarda la email que se pasa como parámetro. Si ya existe actualiza el existente.
         *
         * @param form
         */
        function saveEmail(form) {
            var deferred = $q.defer();

            var email = angular.copy(form);

            api.emails.update(email, updateOK, saveKO);

            return deferred.promise;

            function createOK(response) {
                // Store the clients
                service.emails.data.push(response);
                service.emails.count ++;
                deferred.resolve(response);
            }

            function updateOK(response) {
                // Actauliza el listado
                for (var i = 0; i < service.emails.data.length; i++) {
                    if (service.emails.data[i].id === response.id) {
                        service.emails.data[i] = angular.copy(response);
                    }
                }
                deferred.resolve(response);
            }

            function saveKO(response) {
                deferred.reject(response);
            }

        }

        /**
         * Devuelve un emailo vacío
         */
        function getEmptyEmail() {
            return {
            };
        }

        function removeEmail(email){
            var deferred = $q.defer();

            api.emails.remove({id: email.id}, emailRemoveOK, removeKO);

            // Emailo borrado correctamente
            function emailRemoveOK(response){
                // Quitamos la email en los datos locales
                for (var i = 0; i < service.emails.data.length; i++) {
                    if (service.emails.data[i].id === email.id) {
                        service.emails.data.splice(i,1);
                        service.emails.count -= 1;
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
