(function () {
    'use strict';

    angular
        .module('app.acds')
        .controller('AcdDialogController', AcdDialogController);

    /** @ngInject */
    function AcdDialogController($mdDialog, Acd, acdsService, NotifyService, originsService, $q, gettextCatalog) {
        var vm = this;

        // Data
        vm.title = gettextCatalog.getString('Asignar Lead');
        vm.acd = angular.copy(Acd); // Copiamos para no modificar el original hasta guardar

        // Methods
        vm.saveAcd = saveAcd;
        vm.closeDialog = closeDialog;

        //////////
        /**
         * Guardar acdo
         */
        function saveAcd() {
            return acdsService.saveAcd(angular.copy(vm.acd)).then(function(){
                NotifyService.successMessage(gettextCatalog.getString("Concesionario guardado correctamente"));
                closeDialog();
            }, function(error){
                vm.serverErrors = error.data;
                NotifyService.errorMessage(gettextCatalog.getString("Error al guardar el concesionario.") +" " + (error.data.non_field_errors || ""));
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
