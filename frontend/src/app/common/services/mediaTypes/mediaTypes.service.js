(function () {
    'use strict';

    angular
        .module('app.services')
        .factory('mediaTypesService', mediaTypesService);

    /** @ngInject */
    function mediaTypesService(gettextCatalog) {

        var service = {
            mediaTypes: [
                {
                    id:'Whatsapp',
                    icon:'icon-whatsapp',
                    name:gettextCatalog.getString('Whatsapp'),
                    alias:gettextCatalog.getString('Enviar Whatsapp a')
                },{
                    id:'Phone',
                    icon:'icon-phone',
                    name:gettextCatalog.getString('Teléfono'),
                    alias:gettextCatalog.getString('LLamar a')
                },{
                    id:'SMS',
                    icon:'SMS',
                    name:gettextCatalog.getString('SMS'),
                    alias:gettextCatalog.getString('Enviar SMS a')
                },{
                    id:'E-mail',
                    icon:'icon-email',
                    name:gettextCatalog.getString('Email'),
                    alias:gettextCatalog.getString('Enviar Email a')
                },{
                    id:'face',
                    icon:'icon-account-multiple',
                    name:gettextCatalog.getString('Reunión'),
                    alias:gettextCatalog.getString('Reunión con')
                }
            ]
        };

        return service;

    }

})();
