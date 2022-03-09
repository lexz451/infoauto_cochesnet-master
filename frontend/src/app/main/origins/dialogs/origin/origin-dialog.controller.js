(function () {
    'use strict';

    angular
        .module('app.origins')
        .controller('OriginDialogController', OriginDialogController);

    /** @ngInject */
    function OriginDialogController($scope, $mdDialog, Origin, originsService, channelsService, Channels, NotifyService, $timeout, gettextCatalog) {
        var vm = this;

        // Data
        vm.title = gettextCatalog.getString('Editar origen');
        vm.channels = Channels;

        if (!Origin) {
            vm.title = gettextCatalog.getString('Nuevo origen');
            vm.origin = originsService.getEmptyOrigin();
        } else {
            vm.origin = angular.copy(Origin); // Copiamos para no modificar el original hasta guardar
        }

        $timeout(function () {
            $("#image-uploader").change(function(){
                readURL(this);
            });
        });

        // Methods
        vm.saveOrigin = saveOrigin;
        vm.closeDialog = closeDialog;
        vm.openFiles = openFiles;

        //////////
        /**
         * Guardar origino
         */
        function saveOrigin() {
            return originsService.saveOrigin(angular.copy(vm.origin)).then(function(){
                NotifyService.successMessage(gettextCatalog.getString("Origen guardado correctamente"));
                closeDialog();
            }, function(error){
                vm.serverErrors = error.data;
                NotifyService.errorMessage(gettextCatalog.getString("Error al guardar el origen.") +" "+ (error.data.non_field_errors || ""));
            });
        }

        /**
         * Cerrar el cuadro de diálogo sin cambios
         */
        function closeDialog() {
            $mdDialog.hide();
        }

        /**
         * Image change
         * @param input
         */
        function readURL(input)
        {
            if (input.files && input.files[0]) {
                var reader = new FileReader();

                reader.onload = function (e) {
                    vm.origin.icon = e.target.result;

                    if(!$scope.$$phase) {
                        $scope.$digest();
                    }
                };

                reader.readAsDataURL(input.files[0]);
            }
        }

        /**
         * Open filebrowser
         */
        function openFiles(form)
        {
            form.$setDirty();
            $("#image-uploader").click();
        }

    }
})();
