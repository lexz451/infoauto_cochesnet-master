(function () {
    'use strict';

    angular
        .module('app.concessionaires',
            [

            ]
        )
        .config(config);

    /** @ngInject */
    function config($stateProvider, msApiProvider) {

        // State
        $stateProvider.state('app.concessionaires', {
            url      : '/concessionaires',
            views    : {
                'content@app': {
                    templateUrl: 'app/main/concessionaires/concessionaires.html',
                    controller : 'ConcessionairesController as vm'
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
                Concessionaires: function (concessionairesService) {
                    concessionairesService.concessionaires.filters={};
                    return concessionairesService.getConcessionairesConfig();
                }
            },
            bodyClass: 'todo'
        });


    }
})();
