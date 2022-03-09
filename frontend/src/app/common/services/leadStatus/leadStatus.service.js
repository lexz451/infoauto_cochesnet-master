(function () {
    'use strict';

    angular
        .module('app.services')
        .factory('leadStatusService', leadStatusService);

    /** @ngInject */
    function leadStatusService(gettextCatalog) {

        var service = {
            leadStatus: [
                {
                    id:'new',
                    name:gettextCatalog.getString('Lead no atendido'),
                    color:'#009688'
                },{
                    id:'attended',
                    name:gettextCatalog.getString('Lead atendido por comercial'),
                    color:'#f39400'
                },{
                    id:'commercial_management',
                    name:gettextCatalog.getString('Tareas pendientes'),
                    color:'#2196f3'
                },{
                    id:'tracing',
                    name:gettextCatalog.getString('Seguimiento'),
                    color:'#673ab7'
                },{
                    id:'end',
                    name:gettextCatalog.getString('Lead cerrado'),
                    color:'#f44336'
                }
            ]
        };

        return service;

    }

})();
