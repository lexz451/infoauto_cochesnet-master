(function () {
    'use strict';

    angular
        .module('app.leads')
        .controller('LeadHistoryDialogController', LeadHistoryDialogController);

    /** @ngInject */
    function LeadHistoryDialogController($mdDialog, LeadHistories, NotifyService, gettextCatalog) {
        var vm = this;

        // Data
        vm.title = gettextCatalog.getString('Histórico');
        vm.leadHistories=LeadHistories;

        // Methods
        vm.closeDialog = closeDialog;

        //////////
        
        /**
         * Cerrar el cuadro de diálogo sin cambios
         */
        function closeDialog() {
            $mdDialog.hide();
        }

    }
})();
