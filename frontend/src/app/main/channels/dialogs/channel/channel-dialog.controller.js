(function () {
    'use strict';

    angular
        .module('app.channels')
        .controller('ChannelDialogController', ChannelDialogController);

    /** @ngInject */
    function ChannelDialogController($scope, $mdDialog, Channel, channelsService, NotifyService, $timeout, gettextCatalog) {
        var vm = this;

        // Data
        vm.title = gettextCatalog.getString('Editar canal');

        if (!Channel) {
            vm.title = gettextCatalog.getString('Nuevo canal');
            vm.channel = channelsService.getEmptyChannel();
        } else {
            vm.channel = angular.copy(Channel); // Copiamos para no modificar el channelal hasta guardar
        }

        // Methods
        vm.saveChannel = saveChannel;
        vm.closeDialog = closeDialog;

        //////////
        /**
         * Guardar channelo
         */
        function saveChannel() {
            return channelsService.saveChannel(angular.copy(vm.channel)).then(function(){
                NotifyService.successMessage(gettextCatalog.getString("Canal guardado correctamente"));
                closeDialog();
            }, function(error){
                vm.serverErrors = error.data;
                NotifyService.errorMessage(gettextCatalog.getString("Error al guardar el canal.") +" " + (error.data.non_field_errors || ""));
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
