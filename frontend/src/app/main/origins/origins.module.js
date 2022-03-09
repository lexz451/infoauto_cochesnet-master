(function () {
    'use strict';

    angular
        .module('app.origins',
            [

            ]
        )
        .config(config);

    /** @ngInject */
    function config($stateProvider, msApiProvider) {

        // State
        $stateProvider.state('app.origins', {
            url      : '/origins',
            views    : {
                'content@app': {
                    templateUrl: 'app/main/origins/origins.html',
                    controller : 'OriginsController as vm'
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
                Origins: function (originsService) {
                    originsService.origins.filters={};
                    return originsService.getOrigins();
                }
            },
            bodyClass: 'todo'
        });


    }
})();
