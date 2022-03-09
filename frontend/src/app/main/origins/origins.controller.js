(function ()
{
    'use strict';
    angular
        .module('app.origins')
        .controller('OriginsController', OriginsController);
    /** @ngInject */
    function OriginsController($scope, currentUser, originsService, Origins, NotifyService, $mdDialog, $document,
                               channelsService, DebounceService, gettextCatalog)
    {
        var vm = this;
        // Data
        vm.user = currentUser;
        vm.origins=Origins;

        // Watchers
        $scope.$watch('vm.origins.filters', DebounceService(originsService.getOrigins, 300), true);

        // Methods
        vm.openOriginDialog = openOriginDialog;
        vm.removeOrigin = removeOrigin;

        //////////
        /**
         * Abre el dialogo para crear/editar una origin
         *
         * @param ev
         * @param origin
         */
        function openOriginDialog(ev, origin) {
            $mdDialog.show({
                controller: 'OriginDialogController',
                controllerAs: 'vm',
                templateUrl: 'app/main/origins/dialogs/origin/origin-dialog.html',
                parent: angular.element($document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                locals: {
                    Origin:origin,
                    Channels:channelsService.getAllChannels(),
                    event: ev
                }
            });
        }

      
        /**
         * Abre el dialogo para eliminar una origin
         *
         * @param ev
         * @param origin
         */
        function removeOrigin(ev, origin) {
            var confirm = $mdDialog.confirm()
                .title(gettextCatalog.getString('Eliminar concesionario')+' "'+origin.name+'"')
                .textContent(gettextCatalog.getString('¿Seguro que quieres eliminar el concesionario?'))
                .ariaLabel(gettextCatalog.getString('Eliminar concesionario'))
                .clickOutsideToClose(true)
                .parent(angular.element(document.body))
                .ok(gettextCatalog.getString('Borrar concesionario'))
                .cancel(gettextCatalog.getString('Cancelar'));

            $mdDialog.show(confirm).then(function() {
                originsService.removeOrigin(origin).then(function(){
                    NotifyService.successMessage(gettextCatalog.getString("Concesionario borrado correctamente."));
                }, function(error){
                    NotifyService.errorMessage("Error al borrar el concesionario." +" "+ (error.data.detail || ""));
                });
            });

        }

    }
})();