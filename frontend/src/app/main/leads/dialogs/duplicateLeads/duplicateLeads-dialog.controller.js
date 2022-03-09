(function () {
    'use strict';

    angular
        .module('app.leads')
        .controller('DuplicateLeadsDialogController', DuplicateLeadsDialogController);

    /** @ngInject */
    function DuplicateLeadsDialogController($mdDialog, DuplicateLeads, leadStatusService, $state, gettextCatalog) {
        var vm = this;

        // Data
        vm.title = gettextCatalog.getString('Posible lead duplicado');
        vm.duplicateLeads = DuplicateLeads;
        vm.lead = null;
        vm.status=leadStatusService.leadStatus;

        // Methods
        vm.goToLead = goToLead;
        vm.closeDialog = closeDialog;

        //////////
        /**
         * Guardar duplicateLeadso
         */
        function goToLead() {
            $state.go("app.leads.get.edit",{lead:vm.lead});
            $mdDialog.hide();
        }

        /**
         * Cerrar el cuadro de diálogo sin cambios
         */
        function closeDialog() {
            $mdDialog.hide();
        }

    }
})();
