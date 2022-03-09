(function () {
  'use strict';

  angular
    .module('app.imports')
    .controller('ImportsViewController', ImportsViewController);

  /** @ngInject */
  function ImportsViewController($document, $rootScope, leadsService, NotifyService, $timeout, concessionairesService,
                                 $mdDialog, gettextCatalog) {
    var vm = this;

    // Data
    vm.loadingImport = false;

    // Methods
    vm.getDocument = getDocument;
    vm.openFiles = openFiles;
    vm.importLeads = importLeads;
    vm.openExportLeadDialog = openExportLeadDialog;

    //////////
    init();

    /**
     * Initialize
     */
    function init() {
      $timeout(function () {
        $("#file-uploader").change(function () {
          importLeads()
        });
      });
    }

    //descagar en general de documentos
    function getDocument() {
      return leadsService.getDocument().then(function (response) {
        downloadFile(response, "leads.xls", "leads.xls");
      }, function (error) {
        NotifyService.errorMessage(gettextCatalog.getString("Error al exportar leads"));
      });
    }

    //Descarga cualquier tipo de fichero
    function downloadFile(response, name, type) {
      var blob = new Blob([response], {type: type});

      if (window.navigator && window.navigator.msSaveOrOpenBlob) {
        window.navigator.msSaveOrOpenBlob(blob);
      } else {
        var link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = name;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
    }

    function openFiles() {
      $("#file-uploader").trigger("click");
    }

    /**
     * Importar excel
     */
    function importLeads() {
      vm.loadingImport = true;
      return leadsService.importLeads().then(function (response) {
        NotifyService.successMessage(gettextCatalog.getString("Leads importado correctamente"));
        downloadFile(response, "result.xls", "result.xls");
        vm.loadingImport = false;
      }, function (error) {
        vm.serverErrors = error.data;
        NotifyService.errorMessage(gettextCatalog.getString("Error al importar leads. ") + (error.data.non_field_errors || ""));
        vm.loadingImport = false;
      });
    }

    /**
     * Abre el dialogo para exportar leads
     *
     * @param ev
     */
    function openExportLeadDialog(ev) {
      $rootScope.loadingProgress = true;
      $mdDialog.show({
        controller: 'ExportLeadDialogController',
        controllerAs: 'vm',
        templateUrl: 'app/main/leads/dialogs/exportLeads/exportLeads-dialog.html',
        parent: angular.element($document.body),
        targetEvent: ev,
        clickOutsideToClose: true,
        locals: {
          event: ev,
          Concessionaires: concessionairesService.getAllConcessionaires()
        }
      });
    }
  }
})();
