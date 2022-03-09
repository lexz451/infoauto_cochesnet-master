(function () {
    'use strict';

    angular
        .module('app.leads')
        .controller('LeadStatusDateDialogController', LeadStatusDateDialogController);

    /** @ngInject */
    function LeadStatusDateDialogController($mdDialog, Lead, Field, leadsService, NotifyService, $q, gettextCatalog) {
        var vm = this;

        // Data
        vm.lead={id: Lead.id};
        vm.field='custom_'+Field;
        vm.lead[vm.field]=moment(Lead[Field], "YYYY-MM-DDThh:mm").toDate();

        // Methods
        vm.saveLeadStatus = saveLeadStatus;
        vm.closeDialog = closeDialog;

        //////////
        /**
         * Guardar informe
         */
        function saveLeadStatus() {
            return leadsService.saveLead(angular.copy(vm.lead)).then(function(res){
                NotifyService.successMessage(gettextCatalog.getString("Fecha guardada correctamente"));
                Lead[Field]=res[Field];
                closeDialog();
            }, function(error){
                vm.serverErrors = error.data;
                NotifyService.errorMessage(gettextCatalog.getString("Error al guardar la fecha.") +" "+ (error.data.non_field_errors || ""));
            });
        }

        /**
         * Cerrar el cuadro de diálogo sin cambios
         */
        function closeDialog() {
            $mdDialog.hide();
        }

    }
})();
