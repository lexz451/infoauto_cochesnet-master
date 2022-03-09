(function () {
    'use strict';

    angular
        .module('app.users')
        .controller('AvailableDialogController', AvailableDialogController);

    /** @ngInject */
    function AvailableDialogController($mdDialog, User, usersService, NotifyService, $q, gettextCatalog) {
        var vm = this;

        // Data
        vm.title = gettextCatalog.getString('Disponibilidad');
        vm.form={
            id:User.id,
            is_available:false
        };

        vm.reasons=[
            {id:'asisting_clients' ,name:'Atendiendo clientes'},
            {id:'breakfast', name:'Desayunando'},
            {id:'bathroom', name:'En el aseo'},
            {id:'excused', name:'Ausencia justificada'}
        ]

        // Methods
        vm.saveAvailable = saveAvailable;
        vm.closeDialog = closeDialog;

        //////////
        /**
         * Guardar availableo
         */
        function saveAvailable() {
            return usersService.saveUser(vm.form).then(function(res){
                $mdDialog.hide(res);
            })
        }

        /**
         * Cerrar el cuadro de diálogo sin cambios
         */
        function closeDialog() {
            $mdDialog.hide();
        }


    }
})();
