(function ()
{
    'use strict';
    angular
        .module('app.channels')
        .controller('ChannelsController', ChannelsController);
    /** @ngInject */
    function ChannelsController($scope, currentUser, channelsService, Channels, NotifyService, $mdDialog, $document,
                                        DebounceService, gettextCatalog)
    {
        var vm = this;
        // Data
        vm.user = currentUser;
        vm.channels=Channels;

        // Watchers
        $scope.$watch('vm.channels.filters', DebounceService(channelsService.getChannels, 300), true);

        // Methods
        vm.openChannelDialog = openChannelDialog;
        vm.removeChannel = removeChannel;

        //////////
        /**
         * Abre el dialogo para crear/editar una channel
         *
         * @param ev
         * @param channel
         */
        function openChannelDialog(ev, channel) {
            $mdDialog.show({
                controller: 'ChannelDialogController',
                controllerAs: 'vm',
                templateUrl: 'app/main/channels/dialogs/channel/channel-dialog.html',
                parent: angular.element($document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                locals: {
                    Channel:channel,
                    event: ev
                }
            });
        }

      
        /**
         * Abre el dialogo para eliminar una channel
         *
         * @param ev
         * @param channel
         */
        function removeChannel(ev, channel) {
            var confirm = $mdDialog.confirm()
                .title(gettextCatalog.getString('Eliminar canal')+' "'+channel.name+'"')
                .textContent(gettextCatalog.getString('¿Seguro que quieres eliminar el canal?'))
                .ariaLabel(gettextCatalog.getString('Eliminar canal'))
                .clickOutsideToClose(true)
                .parent(angular.element(document.body))
                .ok(gettextCatalog.getString('Borrar canal'))
                .cancel(gettextCatalog.getString('Cancelar'));

            $mdDialog.show(confirm).then(function() {
                channelsService.removeChannel(channel).then(function(){
                    NotifyService.successMessage(gettextCatalog.getString("Canal borrado correctamente."));
                }, function(error){
                    NotifyService.errorMessage("Error al borrar el canal." +" "+ (error.data.detail || ""));
                });
            });

        }

    }
})();