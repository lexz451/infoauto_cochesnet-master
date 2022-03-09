(function () {
    'use strict';

    angular
        .module('app.services')
        .factory('originsCarService', originsCarService);

    /** @ngInject */
    function originsCarService(gettextCatalog) {

        var service = {
            origins: [
                {
                    id:'national',
                    name:gettextCatalog.getString('Nacional')
                },{
                    id:'foreign',
                    name:gettextCatalog.getString('Extranjero')
                }
            ]
        };

        return service;

    }

})();
