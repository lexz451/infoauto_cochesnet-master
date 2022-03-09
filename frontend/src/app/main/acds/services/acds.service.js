(function () {
    'use strict';

    angular
        .module('app.acds')
        .factory('acdsService', acdsService);

    /** @ngInject */
    function acdsService($q, api, $http, gettextCatalog) {

        var service = {
            acds: {
                data: [],
                count: 0,
                filters: {}
            },
            wsAcds: {
                sockets: []
            },
            socketAcds: socketAcds,
            getAcds: getAcds,
            getAllAcds: getAllAcds,
            getAcd: getAcd,
            saveAcd: saveAcd,
            getEmptyAcd: getEmptyAcd,
            removeAcd: removeAcd,
            getAudio: getAudio,
            getStatusCall: getStatusCall,
            getOriginsCall: getOriginsCall
        };

        return service;

        //////////

        /**
         * Conectamos con el socket
         */
        function socketAcds(user,callback) {
            if(user.is_admin){
                addSocket("admin",callback);
            }else{
                for(var i in user.related_concessionaires){
                    if(user.related_concessionaires[i].concessionaire_data.mask_c2c){
                        addSocket(user.related_concessionaires[i].concessionaire_data.mask_c2c,callback);
                    }
                }

            }
        }

        function addSocket(channel,callback){
            var socket=new ReconnectingWebSocket(api.wsAcds+channel+"/");
            socket.onopen = callback;
            socket.onmessage = callback;

            if ( socket.readyState === WebSocket.OPEN ) {
                socket.onopen();
            }
            service.wsAcds.sockets.push(socket);
        }


        /**
         * Obtiene el listado de acds
         */
        function getAcds() {
            // Create a new deferred object
            var deferred = $q.defer();

            api.acds.get(service.acds.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                service.acds.data=response.results;
                service.acds.count = response.count;

                deferred.resolve(service.acds);
            }

            function getKO(response) {
                //con esto evitamos que den problemas los not found cuando
                // filtramos y estamos en una página que ya no existe
                if(response.status==404 && service.acds.filters.page!=1){
                    service.acds.filters.page=1;
                    getAcds();
                }
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de acds filtrando unicamente por el texto dado y sin guardar en el servicio
         *
         * @param search
         */
        function getAllAcds(search) {
            // Create a new deferred object
            var deferred = $q.defer();
            var f=angular.copy(service.acds.filters);
            f.search=search;
            f.page_size="all";
            api.acds.get(f, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene los datos de una acd determinado por su ID
         *
         * @param id
         */
        function getAcd(id) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.acds.get({id: id}, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Guarda la acd que se pasa como parámetro. Si ya existe actualiza el existente.
         *
         * @param form
         */
        function saveAcd(form) {
            var deferred = $q.defer();

            var acd = angular.copy(form);

            for(var i in acd.phones){
                if(acd.phones[i].origin_data && acd.phones[i].origin_data.id){
                    acd.phones[i].origin=acd.phones[i].origin_data.id;
                }
            }

            if(form.id){
                api.acds.update(acd, updateOK, saveKO);
            }else{
                api.acds.create(acd, createOK, saveKO);
            }

            return deferred.promise;

            function createOK(response) {
                service.getAcds();
                deferred.resolve(response);
            }

            function updateOK(response) {
                // Actauliza el listado
                service.getAcds();
                deferred.resolve(response);
            }

            function saveKO(response) {
                deferred.reject(response);
            }

        }

        /**
         * Devuelve un acdo vacío
         */
        function getEmptyAcd() {
            return {
                phones:[{
                    number:""
                }]
            };
        }

        function removeAcd(acd){
            var deferred = $q.defer();

            api.acds.remove({id: acd.id}, acdRemoveOK, removeKO);

            // Acdo borrado correctamente
            function acdRemoveOK(response){
                // Quitamos la acd en los datos locales
                for (var i = 0; i < service.acds.data.length; i++) {
                    if (service.acds.data[i].id === acd.id) {
                        service.acds.data.splice(i,1);
                        service.acds.count -= 1;
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

        /**
         * Descarga audio de una llamada
         *
         * @param id
         */
        function getAudio(id) {
            var deferred = $q.defer();

            $http.get(api.baseUrl + 'netelip/calls/'+id+'/audio/', {responseType:'arraybuffer',timeout:60*60*1000}).then(getOK, getKO);

            return deferred.promise;

            function getOK(response){
                deferred.resolve(response.data);
            }

            function getKO(response){
                deferred.reject(response);
            }
        }

        function getStatusCall() {
            return [
                {
                    id:'CHANUNAVAIL',
                    name:gettextCatalog.getString('El número llamado no existe'),
                    color:'red-bg'
                },
                {
                    id:'BUSY',
                    name:gettextCatalog.getString('El número llamado está ocupado'),
                    color:'orange-bg'
                },
                {
                    id:'NOANSWER',
                    name:gettextCatalog.getString('El número llamado no contesta'),
                    color:'orange-bg'
                },
                {
                    id:'ANSWER',
                    name:gettextCatalog.getString('El número llamado ha contestado'),
                    color:'green-bg'
                },
                {
                    id:'CANCEL',
                    name:gettextCatalog.getString('El número llamado ha colgado'),
                    color:'orange-bg'
                },
                {
                    id:'CONGESTION',
                    name:gettextCatalog.getString('Fallo en red telefónica por congestión'),
                    color:'red-bg'
                },
                {
                    id:'UNKNOW',
                    name:gettextCatalog.getString('Fallo en red telefónica desconocido'),
                    color:'red-bg'
                },
            ]
        }
        function getOriginsCall() {
            return [
                {
                    id:'user',
                    name:gettextCatalog.getString('Usuario'),
                    color:'teal-bg'
                },
                {
                    id:'client',
                    name:gettextCatalog.getString('Cliente'),
                    color:'green-bg'
                }
            ]
        }


    }

})();
