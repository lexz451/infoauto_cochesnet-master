(function () {
    'use strict';

    angular
        .module('app.leads')
        .factory('leadActionsService', leadActionsService);

    /** @ngInject */
    function leadActionsService($q, api) {

        var service = {
            leadActions: {
                data: [],
                count: 0,
                filters: {}
            },
            getLeadActions: getLeadActions,
            getAllLeadActions: getAllLeadActions,
            getLeadActionsColumn: getLeadActionsColumn,
            getLeadAction: getLeadAction,
            saveLeadAction: saveLeadAction,
            getEmptyLeadAction: getEmptyLeadAction,
            removeLeadAction: removeLeadAction
        };

        return service;

        //////////

        /**
         * Obtiene el listado de leadActions
         */
        function getLeadActions() {
            // Create a new deferred object
            var deferred = $q.defer();
            
            api.leadActions.get(service.leadActions.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                service.leadActions.data = response.results;
                service.leadActions.count = response.count;

                deferred.resolve(service.leadActions);
            }

            function getKO(response) {
                //con esto evitamos que den problemas los not found cuando
                // filtramos y estamos en una página que ya no existe
                if(response.status==404 && service.leadActions.filters.page!=1){
                    service.leadActions.filters.page=1;
                }
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de leadActions filtrando unicamente por el texto dado y sin guardar en el servicio
         *
         * @param search
         */
        function getAllLeadActions(search) {
            // Create a new deferred object
            var deferred = $q.defer();
            var f=angular.copy(service.leadActions.filters);
            f.search=search;
            f.page_size="all";
            api.leadActions.get(f, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de leadActions
         */
        function getLeadActionsColumn() {
            // Create a new deferred object
            var deferred = $q.defer();
            var f={};
            f.page_size="all";
            api.leadActionsColumn.get(f, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene los datos de una leadAction determinado por su ID
         *
         * @param id
         */
        function getLeadAction(id) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.leadActions.get({id: id}, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                service.leadAction.data = response;
                deferred.resolve(response);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Guarda la leadAction que se pasa como parámetro. Si ya existe actualiza el existente.
         *
         * @param form
         */
        function saveLeadAction(form) {
            var deferred = $q.defer();

            var leadAction=angular.copy(form);

            api.leadActions.create(leadAction, createOK, saveKO);

            return deferred.promise;

            function createOK(response) {
                // Store the leadActions
                service.leadActions.data.push(response);
                service.leadActions.count ++;
                deferred.resolve(response);
            }

            function saveKO(response) {
                deferred.reject(response);
            }

        }

        /**
         * Devuelve un leadAction vacío
         */
        function getEmptyLeadAction(lead) {
            return {
                lead: lead.id,
                lead_status_planing: (lead.last_lead_action && lead.last_lead_action.lead_status_planing) ?
                    lead.last_lead_action.lead_status_planing : null,
                date: (lead.last_lead_action && lead.last_lead_action.date) ?
                    moment(lead.last_lead_action.date).toDate() : null
            };
        }
        
        function removeLeadAction(leadAction){
            var deferred = $q.defer();

            api.leadActions.remove({id: leadAction.id}, leadActionRemoveOK, removeKO);

            // LeadAction borrado correctamente
            function leadActionRemoveOK(response){
                // Quitamos la leadAction en los datos locales
                for (var i = 0; i < service.leadActions.data.length; i++) {
                    if (service.leadActions.data[i].id === leadAction.id) {
                        service.leadActions.data.splice(i,1);
                        service.leadActions.count -= 1;
                        break;
                    }
                }
                deferred.resolve(response.data);
            }

            // Fallo al borrar leadAction
            function removeKO(response){
                deferred.reject(response);
            }

            return deferred.promise;
        }

    }


})();
