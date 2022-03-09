(function ()
{
    'use strict';
    angular
        .module('app.videos')
        .controller('VideosController', VideosController);
    /** @ngInject */
    function VideosController($scope, currentUser)
    {
        var vm = this;
        // Data
        vm.user = currentUser;
        vm.videos=[];

        // Methods


        //////////

    }
})();
