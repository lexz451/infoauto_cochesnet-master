(function () {
    'use strict';

    angular
        .module('app.leads')
        .controller('LeadStatusDialogController', LeadStatusDialogController);

    /** @ngInject */
    function LeadStatusDialogController($mdDialog, Lead, leadsService, NotifyService, $q, gettextCatalog) {
        var vm = this;

        // Data
        vm.lead=angular.copy(Lead);
        vm.status=[
            {
                id:'new',
                name:gettextCatalog.getString('Lead no atendido')
            },{
                id:'commercial_management',
                name:gettextCatalog.getString('Tareas pendientes')
            },{
                id:'tracing',
                name:gettextCatalog.getString('Seguimiento')
            }
        ];

        // Methods
        vm.saveLeadStatus = saveLeadStatus;
        vm.closeDialog = closeDialog;

        //////////
        /**
         * Guardar informe
         */
        function saveLeadStatus() {
            return leadsService.changeStatus(angular.copy(vm.lead)).then(function(res){
                NotifyService.successMessage(gettextCatalog.getString("Estado guardado correctamente"));
                Lead.status=res.status;
                closeDialog();
            }, function(error){
                vm.serverErrors = error.data;
                NotifyService.errorMessage(gettextCatalog.getString("Error al guardar el estado.") +" "+ (error.data.non_field_errors || ""));
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
