(function ()
{
    'use strict';

    angular
        .module('fuse')
        .controller('IndexController', IndexController);

    /** @ngInject */
    function IndexController($rootScope, fuseTheming)
    {
        var vm = this;

        // Data
        $rootScope.domain='';
        vm.themes = fuseTheming.themes;
        if(window.location.host.includes("sail") || true){
            fuseTheming.setActiveTheme('sail');
            $rootScope.domain='sail';
        }else{
            fuseTheming.setActiveTheme('default');
        }


    }
})();
