(function ()
{
    'use strict';
    angular
        .module('app.dashboard')
        .controller('DashboardController', DashboardController);
    /** @ngInject */
    function DashboardController($scope, currentUser, $sce, Dashboards, NotifyService, $mdDialog, $document)
    {
        var vm = this;
        // Data
        vm.user = currentUser;
        vm.concessionaires=Dashboards.data;

        // Methods
        vm.trustAsHtml = trustAsHtml;

        //////////

        /**
         * Devuelve el formato necesario para mostrar iframes
         *
         * @param html
         */
        function trustAsHtml(html) {
            return $sce.trustAsHtml(html);
        }


    }
})();