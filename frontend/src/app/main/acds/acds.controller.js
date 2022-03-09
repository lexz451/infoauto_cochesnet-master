(function ()
{
    'use strict';
    angular
        .module('app.acds')
        .controller('AcdsController', AcdsController);
    /** @ngInject */
    function AcdsController($scope, currentUser, acdsService, Acds, NotifyService, $mdDialog, $document, $state,
                            AuthService, DebounceService, gettextCatalog, $timeout)
    {
        var vm = this;
        // Data
        vm.user = currentUser;
        vm.acds=Acds;
        vm.lastAcds=null;
        vm.status=acdsService.getStatusCall();
        vm.origins=acdsService.getOriginsCall();

        AuthService.getCurrentUser().then(function (response) {
            if (response) {
                vm.user=response;
                if(vm.user.id){
                    acdsService.socketAcds(vm.user,reloadAcds);
                }
            }
        });

        // Watchers
        $scope.$watch('vm.acds.filters', DebounceService(acdsService.getAcds, 300), true);

        // Methods
        vm.openAcdDialog = openAcdDialog;
        vm.createLead = createLead;
        vm.getAudio = getAudio;

        //////////
        /**
         * Recarga las llamadas entrantes cuando el socket le avisa
         *
         * @param response
         */
        function reloadAcds(response){
            if(response.data){
                var res=JSON.parse(response.data);
                vm.lastAcds=JSON.parse(res.received_call).ID;
            }
            return acdsService.getAcds().then(function(){
                $timeout(function(){
                    vm.lastAcds=null;
                },2000);
            });
        }

        /**
         * Crea un lead a traves de una llamada entrante
         *
         * @param acd
         */
        function createLead(acd) {
            $state.go("app.leads.get.edit",{lead:0,source:acd.source.id,phone:acd.src,acd:acd.id,user:(acd.user ? acd.user.id: undefined)});
        }

        /**
         * Abre el dialogo para crear/editar una acd
         *
         * @param ev
         * @param acd
         */
        function openAcdDialog(ev, acd) {
            var obj={
                call_control:acd.id,
                possible_leads:acd.possible_leads
            };
            $mdDialog.show({
                controller: 'AcdDialogController',
                controllerAs: 'vm',
                templateUrl: 'app/main/acds/dialogs/acd/acd-dialog.html',
                parent: angular.element($document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                locals: {
                    Acd:obj,
                    event: ev
                }
            });
        }

        /**
         * Abre el dialogo para crear/editar una acd
         *
         * @param acd
         */
        function getAudio(acd) {
            return acdsService.getAudio(acd.id).then(function(response){
                downloadFile(response,acd.src+"-audio.mp3",acd.src+"-audio.mp3");
            }, function(error){
                NotifyService.errorMessage(gettextCatalog.getString("Error al obtener audio"));
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

    }
})();
