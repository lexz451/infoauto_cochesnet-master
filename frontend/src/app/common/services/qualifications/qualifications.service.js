(function () {
    'use strict';

    angular
        .module('app.services')
        .factory('qualificationsService', qualificationsService);

    /** @ngInject */
    function qualificationsService(gettextCatalog) {

        var service = {
            qualifications: [
                {
                    id:'positive',
                    name:gettextCatalog.getString('Positiva')
                },{
                    id:'negative',
                    name:gettextCatalog.getString('Negativa')
                }
            ]
        };

        return service;

    }

})();
