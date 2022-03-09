(function () {
    'use strict';

    angular
        .module('app.channels')
        .factory('channelsService', channelsService);

    /** @ngInject */
    function channelsService($q, api, $http) {

        var service = {
            channels: {
                data: [],
                count: 0,
                filters: {}
            },
            getChannels: getChannels,
            getAllChannels: getAllChannels,
            getChannel: getChannel,
            saveChannel: saveChannel,
            getEmptyChannel: getEmptyChannel,
            removeChannel: removeChannel
        };

        return service;

        //////////

        /**
         * Obtiene el listado de channels
         */
        function getChannels() {
            // Create a new deferred object
            var deferred = $q.defer();

            api.channels.get(service.channels.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                service.channels.data=response.results;
                service.channels.count = response.count;

                deferred.resolve(service.channels);
            }

            function getKO(response) {
                //con esto evitamos que den problemas los not found cuando
                // filtramos y estamos en una página que ya no existe
                if(response.status==404 && service.channels.filters.page!=1){
                    service.channels.filters.page=1;
                    getChannels();
                }
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de channels filtrando unicamente por el texto dado y sin guardar en el servicio
         *
         * @param search
         */
        function getAllChannels(search) {
            // Create a new deferred object
            var deferred = $q.defer();
            var f=angular.copy(service.channels.filters);
            f.search=search;
            f.page_size="all";
            api.channels.get(f, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene los datos de una channel determinado por su ID
         *
         * @param id
         */
        function getChannel(id) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.channels.get({id: id}, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Guarda la channel que se pasa como parámetro. Si ya existe actualiza el existente.
         *
         * @param form
         */
        function saveChannel(form) {
            var deferred = $q.defer();

            var channel = angular.copy(form);

            if(channel.icon && channel.icon.indexOf("http")!==-1){
                delete channel.icon;
            }

            delete channel.phone_set;
            delete channel.email_set;

            if(form.id){
                api.channels.update(channel, updateOK, saveKO);
            }else{
                api.channels.create(channel, createOK, saveKO);
            }

            return deferred.promise;

            function createOK(response) {
                // Store the clients
                service.channels.data.push(response);
                service.channels.count ++;
                deferred.resolve(response);
            }

            function updateOK(response) {
                // Actauliza el listado
                for (var i = 0; i < service.channels.data.length; i++) {
                    if (service.channels.data[i].id === response.id) {
                        service.channels.data[i] = angular.copy(response);
                    }
                }
                deferred.resolve(response);
            }

            function saveKO(response) {
                deferred.reject(response);
            }

        }

        /**
         * Devuelve un channelo vacío
         */
        function getEmptyChannel() {
            return {
            };
        }

        function removeChannel(channel){
            var deferred = $q.defer();

            api.channels.remove({id: channel.id}, channelRemoveOK, removeKO);

            // Channelo borrado correctamente
            function channelRemoveOK(response){
                // Quitamos la channel en los datos locales
                for (var i = 0; i < service.channels.data.length; i++) {
                    if (service.channels.data[i].id === channel.id) {
                        service.channels.data.splice(i,1);
                        service.channels.count -= 1;
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
