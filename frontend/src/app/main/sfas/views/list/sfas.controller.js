(function ()
{
    'use strict';
    angular
        .module('app.sfas')
        .controller('SfasController', SfasController);
    /** @ngInject */
    function SfasController($scope, currentUser, Sfas, usersService, NotifyService, $rootScope, DebounceService,
                            AuthService, $mdDialog, $document, $q, gettextCatalog)
    {
        var vm = this;
        // Data
        vm.user = currentUser;
        vm.sfas=Sfas;

        vm.channels = [
          {id:'email', name:gettextCatalog.getString('Email')},
          {id:'sms', name:gettextCatalog.getString('SMS')}
        ];
        vm.events = [
          {id:'lead_not_attended', name:gettextCatalog.getString('Lead no atendido')},
          {id:'lead_attended', name:gettextCatalog.getString('Lead atendido por usuario')}
        ];

        // Methods
        vm.openSfaDialog = openSfaDialog;
        vm.removeSfa = removeSfa;

        //////////
        /**
         * Abre el dialogo para crear/editar una sfa
         *
         * @param ev
         */
        function openSfaDialog(ev) {
            $mdDialog.show({
                controller: 'SfaDialogController',
                controllerAs: 'vm',
                templateUrl: 'app/main/sfas/dialogs/sfa/sfa-dialog.html',
                parent: angular.element($document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                locals: {
                    User: currentUser,
                    event: ev
                }
            }).then(function() {
                AuthService.checkStatus().then(function (response) {
                    if (response) {
                      vm.sfas=response.sfa_configurations;
                    }
                });
            });
        }

      
        /**
         * Abre el dialogo para eliminar una sfa
         *
         * @param $index
         * @param sfa
         */
        function removeSfa($index, sfa) {
            var confirm = $mdDialog.confirm()
                .title(gettextCatalog.getString('Eliminar automatismo'))
                .textContent(gettextCatalog.getString('¿Seguro que quieres eliminar el automatismo?'))
                .ariaLabel(gettextCatalog.getString('Eliminar automatismo'))
                .clickOutsideToClose(true)
                .parent(angular.element(document.body))
                .ok(gettextCatalog.getString('Borrar automatismo'))
                .cancel(gettextCatalog.getString('Cancelar'));

            $mdDialog.show(confirm).then(function() {
                usersService.removeSFA(angular.copy(sfa)).then(function(){
                    vm.sfas.splice($index,1);
                }, function(error){
                    NotifyService.errorMessage(gettextCatalog.getString("Error al borrar automatísmo.") +" "+ (error.data.non_field_errors || ""));
                });
            });

        }

    }
})();
