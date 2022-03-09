(function () {
    'use strict';

    angular
        .module('app.services')
        .factory('taskTypesService', taskTypesService);

    /** @ngInject */
    function taskTypesService($q, api) {

        var service = {
            getTaskTypes: getTaskTypes,
        };

        return service;

        //////////

        /**
         * Obtiene el listado de taskTypes
         */
        function getTaskTypes(tracing) {
            // Create a new deferred object
            var deferred = $q.defer();

            api.taskTypes.queryAll({is_traking_task:tracing}, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /*var service = {
            taskTypes: [
                {
                    id:'date',
                    name:gettextCatalog.getString('Visita / Test Drive')
                },{
                    id:'appraisal',
                    name:gettextCatalog.getString('Tasación')
                },{
                    id:'budget',
                    name:gettextCatalog.getString('Presupuesto')
                },{
                    id:'financing',
                    name:gettextCatalog.getString('Financiación')
                },{
                    id:'warranty',
                    name:gettextCatalog.getString('Garantía')
                },{
                    id:'vehicle_information',
                    name:gettextCatalog.getString('Información del vehículo')
                },{
                    id: 'response_information_mail',
                    name: gettextCatalog.getString('Responder al Email')
                },{
                    id: 'lost_call',
                    name: gettextCatalog.getString('Atender una llamada perdida')
                },{
                    id: 'send_email',
                    name: gettextCatalog.getString('Enviar email')
                },{
                    id: 'workshop_appointment',
                    name: gettextCatalog.getString('Cita para taller')
                },{
                    id:'other',
                    name:gettextCatalog.getString('Otro')
                }
            ]
        };

        return service;*/

    }

})();
