(function () {
    'use strict';

    angular
        .module('app.acds',
            [

            ]
        )
        .config(config);

    /** @ngInject */
    function config($stateProvider, msApiProvider) {

        // State
        $stateProvider.state('app.acds', {
            url      : '/acds',
            views    : {
                'content@app': {
                    templateUrl: 'app/main/acds/acds.html',
                    controller : 'AcdsController as vm'
                }
            },
            resolve  : {
                currentUser: function (AuthService){
                    return AuthService.getCurrentUser().then(function (response) {
                        if (response) {
                            return response;
                        }
                    });
                },
                Acds: function (acdsService) {
                    acdsService.acds.filters={};
                    return acdsService.getAcds();
                }
            },
            bodyClass: 'todo'
        });


    }
})();
