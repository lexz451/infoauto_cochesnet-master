(function () {
    'use strict';

    angular
        .module('app.leads')
        .controller('ExportLeadDialogController', ExportLeadDialogController);

    /** @ngInject */
    function ExportLeadDialogController($rootScope, $mdDialog, Concessionaires, concessionairesService, NotifyService,
                                        usersService, $q, gettextCatalog) {
        var vm = this;

        // Data
        vm.exportLead={
            created_start_date:new Date(moment().subtract(1, 'months').startOf('day').format()),
            created_end_date:new Date(moment().startOf('day').format())
        };
        vm.title = gettextCatalog.getString('Exportar Leads');
        vm.concessionaires = Concessionaires;
        $rootScope.loadingProgress = false;

        // Methods
        vm.getDocument = getDocument;
        vm.closeDialog = closeDialog;

        //////////
        //descagar en general de documentos
        function getDocument(){
            return concessionairesService.getDocument(vm.exportLead).then(function(response){
                downloadFile(response,"leads.xls","leads.xls");
                closeDialog();
            }, function(error){
                NotifyService.errorMessage(gettextCatalog.getString("Error al exportar leads"));
            });
        }

        //Descarga cualquier tipo de fichero
        function downloadFile(response, name, type) {
            var blob = new Blob([response], {type: type});

            if (window.navigator && window.navigator.msSaveOrOpenBlob) {
                window.navigator.msSaveOrOpenBlob(blob);
            }
            else {
                var link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                link.download = name;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }
        }

        /**
         * Cerrar el cuadro de diálogo sin cambios
         */
        function closeDialog() {
            $mdDialog.hide();
        }

    }
})();
