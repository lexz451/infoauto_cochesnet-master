(function () {
    'use strict';

    angular
        .module('app.videos',
            [

            ]
        )
        .config(config);

    /** @ngInject */
    function config($stateProvider) {

        // State
        $stateProvider.state('app.videos', {
            url      : '/videos',
            views    : {
                'content@app': {
                    templateUrl: 'app/main/videos/videos.html',
                    controller : 'VideosController as vm'
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
