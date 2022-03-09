(function () {
    'use strict';

    angular
        .module('app.leads')
        .controller('SendWhatsappDialogController', SendWhatsappDialogController);

    /** @ngInject */
    function SendWhatsappDialogController($mdDialog, Lead, clientsService, usersService, NotifyService, gettextCatalog) {
        var vm = this;

        // Data
        vm.lead=Lead;
        vm.whatsappMsg='';
        vm.manageTemplates = false;
        vm.newAlias = '';
        vm.newText = '';

        vm.templates = [];

        vm.templateSelected = null;

        // Methods
        vm.sendWhatsapp = sendWhatsapp;
        vm.startManageTemplates = startManageTemplates;
        vm.sendWhatsappTemplates = sendWhatsappTemplates;
        vm.updateTemplate = updateTemplate;
        vm.closeDialog = closeDialog;


        //////////

        /* Send Whatsapp */
        function sendWhatsapp() {
            var msg={message:vm.whatsappMsg, lead:vm.lead.id};
            clientsService.sendWhatsapp(msg).then(function (res) {
                var phone=vm.lead.client.phone;
                var url='https://web.whatsapp.com/send?phone='+phone+'&text='+encodeURIComponent(vm.whatsappMsg);
                window.open(url, '_blank');
                vm.whatsappMsg='';
                closeDialog();
            });
        }

        /* Send Whatsapp */
        function startManageTemplates() {
            vm.templates = angular.copy(Lead.user_data.whatsapp_templates);
            vm.templates.push({
                alias: '',
                text: ''
            });

            vm.manageTemplates = true;
        }

        /* Send Whatsapp */
        function sendWhatsappTemplates() {
            var newTemplates = [];
            for (var i in vm.templates) {
                if (vm.templates[i].alias !== '') {
                    newTemplates.push({
                        id: vm.templates[i].id,
                        alias: vm.templates[i].alias,
                        text: vm.templates[i].text,
                        user: vm.lead.user
                    });
                }
            }

            return usersService.saveUser({whatsapp_templates: newTemplates, email: vm.lead.user_data.email, id: vm.lead.user}).then(function(){
                NotifyService.successMessage(gettextCatalog.getString("Plantillas guardadas correctamente"));
                vm.lead.user_data.whatsapp_templates = newTemplates;
                vm.manageTemplates = false;
            }, function(error){
                vm.serverErrors = error.data;
                NotifyService.errorMessage(gettextCatalog.getString("Error al guardar las plantillas.") +" "+ (error.data.non_field_errors || ""));
            });

        }

        /**
         * Cerrar el cuadro de diálogo sin cambios
         */
        function closeDialog() {
            $mdDialog.hide();
        }

        function updateTemplate()
        {
            // VARIABLE ALIAS VARIABLE
            // [user_user]!first_name & [user_user]!last_name Nombre vendedor
            // [leads_client]!client_name Nombre del cliente
            // [user_user]!phone Telefono del vendedor
            // "[leads_vehicle]! vehiclebrand_model & "" ""
            // [leads_vehicle]! vehicle model & "" ""
            // [leads_vehicle]! vehicle__price" Vehículo solicitado
            // [leads_origin]!name Origen del lead
            // [leads_vehicle]!vehicle_ad_link url anuncio
            // [leads_concessionaire]!name nombre del concesionario

            if(vm.templateSelected) {
                vm.whatsappMsg = vm.templateSelected;
                vm.whatsappMsg = vm.whatsappMsg.replaceAll('[Nombre vendedor]', vm.lead.user_data.first_name + ' ' + vm.lead.user_data.last_name);
                vm.whatsappMsg = vm.whatsappMsg.replaceAll('[Telefono del vendedor]', vm.lead.user_data.phone);
                if (vm.lead.vehicles.length > 0) {
                    var v = '';
                    if (vm.lead.vehicles[0].brand_model) {
                        v = vm.lead.vehicles[0].brand_model.split('__')[0];
                    }
                    if (vm.lead.vehicles[0].model) {
                        v += ' ' + vm.lead.vehicles[0].model.split('__')[0];
                    }
                    if (vm.lead.vehicles[0].price) {
                        v += ' ' + vm.lead.vehicles[0].price + " €";
                    }
                    vm.whatsappMsg = vm.whatsappMsg.replaceAll('[Vehículo solicitado]', v);
                    if (vm.lead.vehicles[0].ad_link) {
                        vm.whatsappMsg = vm.whatsappMsg.replaceAll('[Url anuncio]', vm.lead.vehicles[0].ad_link);
                    }

                }
                if (vm.lead.origin) {
                    vm.whatsappMsg = vm.whatsappMsg.replaceAll('[Origen del lead]', vm.lead.origin.name);
                }
                if (vm.lead.concessionaire_data) {
                    vm.whatsappMsg = vm.whatsappMsg.replaceAll('[Nombre del concesionario]', vm.lead.concessionaire_data.name);
                }

            }
        }
    }
})();
