(function () {
    'use strict';

    angular
        .module('app.sfas')
        .controller('SfaDialogController', SfaDialogController);

    /** @ngInject */
    function SfaDialogController($mdDialog, User, usersService, NotifyService, channelsService, concessionairesService, $q, gettextCatalog) {
        var vm = this;

        // Data
        vm.title = gettextCatalog.getString('Nuevo automatismo');
        vm.channels = [
            {id:'email', name:gettextCatalog.getString('Email')},
            {id:'sms', name:gettextCatalog.getString('SMS')}
        ];
        vm.events = [
            {id:'lead_not_attended', name:gettextCatalog.getString('Lead no atendido')},
            {id:'lead_attended', name:gettextCatalog.getString('Lead atendido por usuario')}
        ];

        vm.user = angular.copy(User); // Copiamos para no modificar el original hasta guardar
        vm.user.sfa_configurations.push({});

        // Methods
        vm.saveUser = saveUser;
        vm.removeSFA = removeSFA;
        vm.closeDialog = closeDialog;

        //////////
        /**
         * Guardar usero
         */
        function saveUser() {
            return usersService.saveUser(angular.copy(vm.user)).then(function(){
                NotifyService.successMessage(gettextCatalog.getString("Automatismo guardado correctamente"));
                closeDialog();
            }, function(error){
                vm.serverErrors = error.data;
                NotifyService.errorMessage(gettextCatalog.getString("Error al guardar el automatismo.") +" "+ (error.data.non_field_errors || ""));
            });
        }

        /**
         * Cerrar el cuadro de diálogo sin cambios
         */
        function closeDialog() {
            $mdDialog.hide();
        }
        /**
         * Borra un SFA
         */
        function removeSFA($index,form, item) {
            return usersService.removeSFA(angular.copy(item)).then(function(){
                form.$setDirty();
                vm.user.sfa_configurations.splice($index,1);
            }, function(error){
                NotifyService.errorMessage(gettextCatalog.getString("Error al borrar SFA.") +" "+ (error.data.non_field_errors || ""));
            });
        }

    }
})();
