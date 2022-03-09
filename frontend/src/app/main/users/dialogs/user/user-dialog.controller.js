(function () {
    'use strict';

    angular
        .module('app.users')
        .controller('UserDialogController', UserDialogController);

    /** @ngInject */
    function UserDialogController($mdDialog, User, usersService, NotifyService, channelsService, concessionairesService, $q, gettextCatalog) {
        var vm = this;

        // Data
        vm.title = gettextCatalog.getString('Editar usuario');
        vm.channels = [
            {id:'email', name:gettextCatalog.getString('Email')},
            {id:'sms', name:gettextCatalog.getString('SMS')}
        ];
        vm.events = [
            {id:'lead_not_attended', name:gettextCatalog.getString('Lead no atendido')},
            {id:'lead_attended', name:gettextCatalog.getString('Lead atendido por usuario')}
        ];

        if (!User) {
            vm.title = gettextCatalog.getString('Nuevo usuario');
            vm.user = usersService.getEmptyUser();
        } else {
            vm.user = angular.copy(User); // Copiamos para no modificar el original hasta guardar
            vm.user.start_date= moment(vm.user.start_date).toDate();
            vm.user.end_date= moment(vm.user.end_date).toDate();
        }

        // Methods
        vm.saveUser = saveUser;
        vm.closeDialog = closeDialog;
        vm.getConcessionaires = getConcessionaires;
        vm.addConcessionaire = addConcessionaire;
        vm.removeConcessionaire = removeConcessionaire;
        vm.addSFA = addSFA;
        vm.removeSFA = removeSFA;

        //////////
        /**
         * Guardar usero
         */
        function saveUser() {
            return usersService.saveUser(angular.copy(vm.user)).then(function(){
                NotifyService.successMessage(gettextCatalog.getString("Usuario guardado correctamente"));
                closeDialog();
            }, function(error){
                vm.serverErrors = error.data;
                NotifyService.errorMessage(gettextCatalog.getString("Error al guardar el usuario.") +" "+ (error.data.non_field_errors || ""));
            });
        }

        /**
         * Cerrar el cuadro de diálogo sin cambios
         */
        function closeDialog() {
            $mdDialog.hide();
        }

        /* Concesionarios */
        function getConcessionaires(searchText) {
            var deferred = $q.defer();
            concessionairesService.concessionaires.filters={};
            concessionairesService.getAllConcessionaires(searchText).then(function(concessionaires){
                deferred.resolve(concessionaires);
            });
            return deferred.promise;
        }

        /**
         * Añade un concesionario
         */
        function addConcessionaire() {
            vm.user.related_concessionaires.push({});
        }

        /**
         * Borra un concesionario
         */
        function removeConcessionaire($index,form, item) {
            if(item.id){
                return usersService.removeConcessionaire(angular.copy(item)).then(function(){
                    form.$setDirty();
                    vm.user.related_concessionaires.splice($index,1);
                }, function(error){
                    NotifyService.errorMessage(gettextCatalog.getString("Error al borrar concesionario.") +" "+ (error.data.non_field_errors || ""));
                });
            }else{
                form.$setDirty();
                vm.user.related_concessionaires.splice($index,1);
            }
        }

        /**
         * Añade un SFA
         */
        function addSFA() {
            vm.user.sfa_configurations.push({});
        }

        /**
         * Borra un SFA
         */
        function removeSFA($index,form, item) {
            if(item.id){
                return usersService.removeSFA(angular.copy(item)).then(function(){
                    form.$setDirty();
                    vm.user.sfa_configurations.splice($index,1);
                }, function(error){
                    NotifyService.errorMessage(gettextCatalog.getString("Error al borrar SFA.") +" "+ (error.data.non_field_errors || ""));
                });
            }else{
                form.$setDirty();
                vm.user.sfa_configurations.splice($index,1);
            }
        }

    }
})();
