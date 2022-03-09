(function () {
    'use strict';

    angular
        .module('app.leads')
        .controller('LeadController', LeadController);

    /** @ngInject */
    function LeadController($rootScope, currentUser, Lead, leadsService, NotifyService,
                               $document, $state, $mdDialog, gettextCatalog) {
        var vm = this;

        // Data
        vm.user=currentUser;
        vm.lead = angular.copy(Lead);

        // Methods

        //////////


    }
})();
