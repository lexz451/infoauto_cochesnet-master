(function ()
{
    'use strict';
    angular
        .module('app.concessionaires')
        .controller('ConcessionairesController', ConcessionairesController);
    /** @ngInject */
    function ConcessionairesController($scope, currentUser, concessionairesService, Concessionaires, NotifyService, $mdDialog, $document,
                                        DebounceService, gettextCatalog)
    {
        var vm = this;
        // Data
        vm.user = currentUser;
        vm.concessionaires=Concessionaires;

        // Watchers
        $scope.$watch('vm.concessionaires.filters', DebounceService(concessionairesService.getConcessionairesConfig, 300), true);

        // Methods
        vm.openConcessionaireDialog = openConcessionaireDialog;
        vm.openConcessionaireCalendarDialog = openConcessionaireCalendarDialog;
        vm.openConcessionaireNotesDialog = openConcessionaireNotesDialog;
        vm.removeConcessionaire = removeConcessionaire;

        //////////
        /**
         * Abre el dialogo para crear/editar una concessionaire
         *
         * @param ev
         * @param concessionaire
         */
        function openConcessionaireDialog(ev, concessionaire) {
            $mdDialog.show({
                controller: 'ConcessionaireDialogController',
                controllerAs: 'vm',
                templateUrl: 'app/main/concessionaires/dialogs/concessionaire/concessionaire-dialog.html',
                parent: angular.element($document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                locals: {
                    Concessionaire:concessionaire,
                    event: ev
                }
            });
        }

        /**
         * Abre el dialogo para editar el calendario de un concessionaire
         *
         * @param ev
         * @param concessionaire
         */
        function openConcessionaireCalendarDialog(ev, concessionaire) {
            $mdDialog.show({
                controller: 'ConcessionaireCalendarDialogController',
                controllerAs: 'vm',
                templateUrl: 'app/main/concessionaires/dialogs/concessionaireCalendar/concessionaireCalendar-dialog.html',
                parent: angular.element($document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                locals: {
                    Concessionaire:concessionaire,
                    event: ev
                }
            });
        }

        /**
         * Abre el dialogo para editar el calendario de un concessionaire
         *
         * @param ev
         * @param concessionaire
         */
        function openConcessionaireNotesDialog(ev, concessionaire) {
            $mdDialog.show({
                controller: 'ConcessionaireNotesDialogController',
                controllerAs: 'vm',
                templateUrl: 'app/main/concessionaires/dialogs/concessionaireNotes/concessionaireNotes-dialog.html',
                parent: angular.element($document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                locals: {
                    Concessionaire:concessionaire,
                    event: ev
                }
            });
        }

      
        /**
         * Abre el dialogo para eliminar una concessionaire
         *
         * @param ev
         * @param concessionaire
         */
        function removeConcessionaire(ev, concessionaire) {
            var confirm = $mdDialog.confirm()
                .title(gettextCatalog.getString('Eliminar concesionario')+' "'+concessionaire.name+'"')
                .textContent(gettextCatalog.getString('¿Seguro que quieres eliminar el concesionario?'))
                .ariaLabel(gettextCatalog.getString('Eliminar concesionario'))
                .clickOutsideToClose(true)
                .parent(angular.element(document.body))
                .ok(gettextCatalog.getString('Borrar concesionario'))
                .cancel(gettextCatalog.getString('Cancelar'));

            $mdDialog.show(confirm).then(function() {
                concessionairesService.removeConcessionaire(concessionaire).then(function(){
                    NotifyService.successMessage(gettextCatalog.getString("Concesionario borrado correctamente."));
                }, function(error){
                    NotifyService.errorMessage("Error al borrar el concesionario." +" "+ (error.data.detail || ""));
                });
            });

        }

    }
})();