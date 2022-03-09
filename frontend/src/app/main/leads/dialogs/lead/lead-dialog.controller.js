(function () {
    'use strict';

    angular
        .module('app.leads')
        .controller('LeadDialogController', LeadDialogController);

    /** @ngInject */
    function LeadDialogController($mdDialog, Lead, leadsService, Concessionaire, NotifyService, usersService, $q, Users, gettextCatalog) {
        var vm = this;

        // Data
        vm.lead={
            user:Lead.user,
            user_data:Lead.user_data,
            id:Lead.id,
            source_data_prov:Lead.source_data_prov
        };

        vm.users=Users;

        vm.title = gettextCatalog.getString('Asignar comercial');

        // Methods
        vm.saveLead = saveLead;
        vm.getFullUserName = getFullUserName;
        vm.closeDialog = closeDialog;

        //////////
        /**
         * Guardar informe
         */
        function saveLead(user) {
            if(user && user.id){
                vm.lead.user=user.id;
                vm.lead.user_data=user;
                return leadsService.saveLead(angular.copy(vm.lead)).then(function(res){
                    NotifyService.successMessage(gettextCatalog.getString("Infome guardado correctamente"));
                    Lead.status=res.status;
                    Lead.end_date=res.end_date;
                    Lead.user_data=res.user_data;
                    closeDialog();
                }, function(error){
                    vm.serverErrors = error.data;
                    NotifyService.errorMessage(gettextCatalog.getString("Error al guardar el infome.") +" "+ (error.data.non_field_errors || ""));
                });
            }else{
                NotifyService.errorMessage(gettextCatalog.getString("Debe seleccionar un comercial existente. "));
            }

        }

        function getFullUserName(user) {
            if(user){
                return user.first_name+" "+user.last_name;
            }
            return '';
        }
        
        /**
         * Cerrar el cuadro de diálogo sin cambios
         */
        function closeDialog() {
            $mdDialog.hide();
        }

    }
})();
