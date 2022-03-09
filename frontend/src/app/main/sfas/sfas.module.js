(function () {
    'use strict';

    angular
        .module('app.sfas',
            [

            ]
        )
        .config(config);

    /** @ngInject */
    function config($stateProvider) {

        $stateProvider
            .state('app.sfas', {
                abstract: true,
                url: '/sfas',
                resolve:{
                    currentUser: function (AuthService){
                        return AuthService.checkStatus().then(function (response) {
                            if (response) {
                                return response;
                            }
                        });
                    }
                }
            })
            .state('app.sfas.list', {
                url: '/',
                views: {
                    'content@app': {
                        templateUrl: 'app/main/sfas/views/list/sfas.html',
                        controller: 'SfasController as vm'
                    }
                },
                resolve: {
                    Sfas: function (currentUser) {
                        return currentUser.sfa_configurations;
                    }
                },
                bodyClass: 'sfas'
            })

    }
})();
