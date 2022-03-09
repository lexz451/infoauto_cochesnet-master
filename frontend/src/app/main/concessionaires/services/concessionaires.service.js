(function () {
    'use strict';

    angular
        .module('app.concessionaires')
        .factory('concessionairesService', concessionairesService);

    /** @ngInject */
    function concessionairesService($q, api, $http) {

        var service = {
            concessionaires: {
                data: [],
                count: 0,
                filters: {}
            },
            getConcessionaires: getConcessionaires,
            getConcessionairesConfig: getConcessionairesConfig,
            getAllConcessionaires: getAllConcessionaires,
            getConcessionaire: getConcessionaire,
            saveConcessionaire: saveConcessionaire,
            getEmptyConcessionaire: getEmptyConcessionaire,
            removeConcessionaire: removeConcessionaire,
            removeSource: removeSource,
            getDocument: getDocument
        };

        return service;

        //////////

        /**
         * Obtiene el listado de concessionaires
         */
        function getConcessionaires() {
            // Create a new deferred object
            var deferred = $q.defer();

            api.concessionaires.get(service.concessionaires.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                service.concessionaires.data=response.results;
                service.concessionaires.count = response.count;

                deferred.resolve(service.concessionaires);
            }

            function getKO(response) {
                //con esto evitamos que den problemas los not found cuando
                // filtramos y estamos en una página que ya no existe
                if(response.status==404 && service.concessionaires.filters.page!=1){
                    service.concessionaires.filters.page=1;
                    getConcessionaires();
                }
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de concessionaires
         */
        function getConcessionairesConfig() {
            // Create a new deferred object
            var deferred = $q.defer();

            api.concessionaires.config(service.concessionaires.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                service.concessionaires.data=response.results;
                service.concessionaires.count = response.count;

                deferred.resolve(service.concessionaires);
            }

            function getKO(response) {
                //con esto evitamos que den problemas los not found cuando
                // filtramos y estamos en una página que ya no existe
                if(response.status==404 && service.concessionaires.filters.page!=1){
                    service.concessionaires.filters.page=1;
                    getConcessionaires();
                }
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de concessionaires filtrando unicamente por el texto dado y sin guardar en el servicio
         *
         * @param search
         */
        function getAllConcessionaires(search) {
            // Create a new deferred object
            var deferred = $q.defer();
            var f=angular.copy(service.concessionaires.filters);
            f.search=search;
            f.page_size="all";
            api.concessionaires.config(f, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene los datos de una concessionaire determinado por su ID
         *
         * @param id
         */
        function getConcessionaire(id) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.concessionaires.get({id: id}, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Guarda la concessionaire que se pasa como parámetro. Si ya existe actualiza el existente.
         *
         * @param form
         */
        function saveConcessionaire(form) {
            var deferred = $q.defer();

            var concessionaire = angular.copy(form);

            for(var i in concessionaire.sources){
                if(concessionaire.sources[i].origin_data && concessionaire.sources[i].origin_data.id){
                    concessionaire.sources[i].origin=concessionaire.sources[i].origin_data.id;
                }
                if(concessionaire.sources[i].channel_data && concessionaire.sources[i].channel_data.id){
                    concessionaire.sources[i].channel=concessionaire.sources[i].channel_data.id;
                }
            }

            if(form.id){
                api.concessionaires.update(concessionaire, updateOK, saveKO);
            }else{
                api.concessionaires.create(concessionaire, createOK, saveKO);
            }

            return deferred.promise;

            function createOK(response) {
                // Store the clients
                service.concessionaires.data.push(response);
                service.concessionaires.count ++;
                deferred.resolve(response);
            }

            function updateOK(response) {
                // Actauliza el listado
                for (var i = 0; i < service.concessionaires.data.length; i++) {
                    if (service.concessionaires.data[i].id === response.id) {
                        service.concessionaires.data[i] = angular.copy(response);
                    }
                }
                deferred.resolve(response);
            }

            function saveKO(response) {
                deferred.reject(response);
            }

        }

        /**
         * Devuelve un concessionaireo vacío
         */
        function getEmptyConcessionaire() {
            return {
                phones:[{
                    number:""
                }],
                emails:[],
                sources:[]
            };
        }

        function removeConcessionaire(concessionaire){
            var deferred = $q.defer();

            api.concessionaires.remove({id: concessionaire.id}, concessionaireRemoveOK, removeKO);

            // Concessionaireo borrado correctamente
            function concessionaireRemoveOK(response){
                // Quitamos la concessionaire en los datos locales
                for (var i = 0; i < service.concessionaires.data.length; i++) {
                    if (service.concessionaires.data[i].id === concessionaire.id) {
                        service.concessionaires.data.splice(i,1);
                        service.concessionaires.count -= 1;
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

        function removeSource(item){
            var deferred = $q.defer();

            api.concessionaires.removeSource({id: item.id}, removeOK, removeKO);

            // borrado correctamente
            function removeOK(response){
                deferred.resolve(response.data);
            }

            // Fallo al borrar
            function removeKO(response){
                deferred.reject(response);
            }

            return deferred.promise;
        }

        /**
         * Descarga un documento excel con leads de los concesionarios pasados como parámetro
         *
         * @param params
         */
        function getDocument(params) {
            var deferred = $q.defer();
            params.page_size='all';

            $http({
                url: api.baseUrl + 'lead/excel/',
                method: "GET",
                params: params,
                responseType:'arraybuffer',
                timeout:60*60*1000
            }).then(getOK, getKO);

            return deferred.promise;

            function getOK(response){
                deferred.resolve(response.data);
            }

            function getKO(response){
                deferred.reject(response);
            }
        }


    }

})();
