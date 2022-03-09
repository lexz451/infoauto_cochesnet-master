(function () {
    'use strict';

    angular
        .module('app.leads')
        .controller('SaveLeadDialogController', SaveLeadDialogController);

    /** @ngInject */
    function SaveLeadDialogController($mdDialog, Lead, Tasks, leadsService, leadActionsService, taskTypesService,
                                      NotifyService, $q, $state, $timeout, tasksService, gettextCatalog) {
        var vm = this;

        // Data
        vm.lead=Lead;
        vm.tasks=Tasks;
        vm.leadAction=leadActionsService.getEmptyLeadAction(Lead);
        vm.taskTypes=taskTypesService.taskTypes;

        // Methods
        vm.saveSaveLead = saveSaveLead;
        vm.closeDialog = closeDialog;
        vm.finishLead = finishLead;
        vm.setDate = setDate;

        //////////

        /**
         * Guardar informe
         */
        function saveSaveLead() {
            var deferred = $q.defer();

            var obj=angular.copy(vm.lead);
            delete obj.request;

            leadsService.saveLead(obj).then(function(response){

                leadActionsService.saveLeadAction(vm.leadAction).then(function(response){
                    closeDialog();
                    $timeout(function(){
                        $state.go("app.leads.board");
                    },500);
                    NotifyService.successMessage(gettextCatalog.getString("Informe guardado correctamente"));
                    deferred.resolve(response);

                }, function(error){
                    saveKO(error);
                    deferred.reject(error);
                });

            }, function(error){
                saveKO(error);
                deferred.reject(error);
            });

            return deferred.promise;
        }

        /**
         * Finaliza el informe
         */
        function finishLead() {
            var deferred = $q.defer();
            leadsService.getLead(vm.lead.id).then(function(res){
                if(res.pending_tasks){
                    var confirm = $mdDialog.confirm()
                        .title(gettextCatalog.getString('Finalizar lead'))
                        .textContent(gettextCatalog.getString('Tienes tareas pendientes de realización y seguimiento ¿Estás seguro de querer finalizar el lead?'))
                        .ariaLabel(gettextCatalog.getString('Finalizar lead'))
                        .clickOutsideToClose(true)
                        .parent(angular.element(document.body))
                        .ok(gettextCatalog.getString('Confirmar'))
                        .cancel(gettextCatalog.getString('Cancelar'));

                    $mdDialog.show(confirm).then(function () {
                        //Abrimos el modal de resultados de gestion
                        openFinishLeadDialog();
                    });
                }else{
                    //Abrimos el modal de resultados de gestion
                    openFinishLeadDialog();
                }
                deferred.resolve();
            },function(){
                deferred.reject();
            });
            return deferred.promise;
        }

        /**
         * Abre el dialogo para indicar el resultado del lead
         */
        function openFinishLeadDialog(lead){
            lead = typeof lead !== 'undefined' ? lead : vm.lead;
            $mdDialog.show({
                controller: 'FinishLeadDialogController',
                controllerAs: 'vm',
                templateUrl: 'app/main/leads/dialogs/finishLead/finishLead-dialog.html',
                parent: angular.element(document.body),
                clickOutsideToClose: true,
                locals: {
                    Lead:lead
                }
            });
        }

        function saveKO(error){
            vm.serverErrors = error.data;
            NotifyService.errorMessage(gettextCatalog.getString("Error al guardar el informe.")+" " + (error.data.non_field_errors || ""));
        }

        /**
         * Cerrar el cuadro de diálogo sin cambios
         */
        function closeDialog() {
            $mdDialog.hide();
        }

        function setDate(days) {
            var today = new Date();
            vm.leadAction.date = new Date(today.getFullYear(), today.getMonth(), today.getDate() + days, 9, 0);
        }

    }
})();
