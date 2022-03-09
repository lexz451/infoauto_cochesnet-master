(function () {
    'use strict';

    angular
        .module('app.leads')
        .controller('LeadContactDialogController', LeadContactDialogController);

    /** @ngInject */
    function LeadContactDialogController($mdDialog, LeadContacts, NotifyService, gettextCatalog) {
        var vm = this;

        // Data
        vm.title = gettextCatalog.getString('Historial de contactos');
        vm.leadContacts=LeadContacts;

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
