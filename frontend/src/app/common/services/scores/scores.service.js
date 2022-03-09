(function () {
    'use strict';

    angular
        .module('app.services')
        .factory('scoresService', scoresService);

    /** @ngInject */
    function scoresService(gettextCatalog) {

        var service = {
            scores: [
                {
                    id:'1',
                    color:"#ea5242",
                    name:gettextCatalog.getString('Muy bajo')
                },{
                    id:'2',
                    color:"#feca15",
                    name:gettextCatalog.getString('Bajo')
                },{
                    id:'3',
                    color:"#8dbf22",
                    name:gettextCatalog.getString('Medio')
                },{
                    id:'4',
                    color:"#3fab34",
                    name:gettextCatalog.getString('Alto')
                }
            ]
        };

        return service;

    }

})();
