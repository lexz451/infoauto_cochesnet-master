(function () {
    'use strict';

    angular
        .module('app.leads')
        .controller('LeadActivityDialogController', LeadActivityDialogController);

    /** @ngInject */
    function LeadActivityDialogController($mdDialog, LeadActivities, NotifyService, gettextCatalog) {
        var vm = this;

        // Data
        vm.title = gettextCatalog.getString('Actividades');
        vm.leadActivities=LeadActivities;

        vm.activityStatus=[
            {
                id:'commercial_management',
                name:gettextCatalog.getString('En gestión')
            },{
                id:'tracing',
                name:gettextCatalog.getString('Seguimiento')
            }
        ];

        // Methods
        vm.closeDialog = closeDialog;

        //////////
        
        /**
         * Cerrar el cuadro de diálogo sin cambios
         */
        function closeDialog() {
            $mdDialog.hide();
        }

    }
})();
