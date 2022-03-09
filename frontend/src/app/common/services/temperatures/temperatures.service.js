(function () {
    'use strict';

    angular
        .module('app.services')
        .factory('temperaturesService', temperaturesService);

    /** @ngInject */
    function temperaturesService(gettextCatalog) {

        var service = {
            temperatures: [
                {
                    id:'30',
                    name:gettextCatalog.getString('Menos de 30')
                },{
                    id:'90',
                    name:'30 - 90'
                },{
                    id:'120',
                    name:'90 - 120'
                },{
                    id:'240',
                    name:'120 - 240'
                }
            ]
        };

        return service;

    }

})();
