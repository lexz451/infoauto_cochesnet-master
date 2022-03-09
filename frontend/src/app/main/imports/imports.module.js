(function () {
    'use strict';

    angular
        .module('app.imports',
            [

            ]
        )
        .config(config);

    /** @ngInject */
    function config($stateProvider) {

        // State
        $stateProvider.state('app.imports', {
            url      : '/imports',
            views    : {
                'content@app': {
                    templateUrl: 'app/main/imports/imports-view.html',
                    controller : 'ImportsViewController as vm'
                }
            },
            resolve  : {
                currentUser: function (AuthService){
                    return AuthService.getCurrentUser().then(function (response) {
                        if (response) {
                            return response;
                        }
                    });
                }
            },
            bodyClass: 'todo'
        });


    }
})();
