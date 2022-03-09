(function () {
    'use strict';

    angular
        .module('app.channels',
            [

            ]
        )
        .config(config);

    /** @ngInject */
    function config($stateProvider, msApiProvider) {

        // State
        $stateProvider.state('app.channels', {
            url      : '/channels',
            views    : {
                'content@app': {
                    templateUrl: 'app/main/channels/channels.html',
                    controller : 'ChannelsController as vm'
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
                Channels: function (channelsService) {
                    channelsService.channels.filters={};
                    return channelsService.getChannels();
                }
            },
            bodyClass: 'todo'
        });


    }
})();
