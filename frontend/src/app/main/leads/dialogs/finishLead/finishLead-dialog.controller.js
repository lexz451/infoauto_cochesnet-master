(function () {
    'use strict';

    angular
        .module('app.leads')
        .controller('FinishLeadDialogController', FinishLeadDialogController);

    /** @ngInject */
    function FinishLeadDialogController($mdDialog, Lead, leadsService, leadResultsService, NotifyService, $state, gettextCatalog) {
        var vm = this;

        // Data
        vm.lead={
            result:null,
            result_reason:null,
            id:Lead.id
        };

        vm.title = gettextCatalog.getString('Finalizar');
        vm.actionError=false;
        vm.buttonErros=leadResultsService.leadResultsErrors;

        // Methods
        vm.saveLead = saveLead;
        vm.saveLeadError = saveLeadError;
        vm.closeDialog = closeDialog;

        //////////
        /**
         * Guardar informe
         */
        function saveLead(result) {
            vm.lead.result=result;

            if(result==='negative' || result==='not_available' || result==='error'){
                vm.actionError=true;
                NotifyService.successMessage(gettextCatalog.getString("Elija una opción"));
                return;
            }

            return leadsService.saveLead(angular.copy(vm.lead)).then(function(res){
                NotifyService.successMessage(gettextCatalog.getString("Lead finalizado correctamente"));
                // Lead.result=res.result;
                // Lead.status=res.status;
                // Lead.status_dates=res.status_dates;
                $state.go("app.leads.board");
                closeDialog();
            }, function(error){
                vm.serverErrors = error.data;
                NotifyService.errorMessage(gettextCatalog.getString("Error al finalizar lead.") +" "+ (error.data.non_field_errors || ""));
            });
        }

        /**
         * Guardar informe
         */
        function saveLeadError(result) {
            vm.lead.result_reason=result;

            return leadsService.saveLead(angular.copy(vm.lead)).then(function(res){
                NotifyService.successMessage(gettextCatalog.getString("Lead finalizado correctamente"));
                // Lead.result=res.result;
                // Lead.status=res.status;
                // Lead.status_dates=res.status_dates;
                $state.go("app.leads.board");
                closeDialog();
            }, function(error){
                vm.serverErrors = error.data;
                NotifyService.errorMessage(gettextCatalog.getString("Error al finalizar lead.") +" "+ (error.data.non_field_errors || ""));
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
