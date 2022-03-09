(function () {
    'use strict';

    angular
        .module('app.concessionaires')
        .controller('ConcessionaireDialogController', ConcessionaireDialogController);

    /** @ngInject */
    function ConcessionaireDialogController($mdDialog, Concessionaire, concessionairesService, NotifyService, originsService, channelsService, $q, gettextCatalog) {
        var vm = this;

        // Data
        vm.title = gettextCatalog.getString('Editar concesionario');

        if (!Concessionaire) {
            vm.title = gettextCatalog.getString('Nuevo concesionario');
            vm.concessionaire = concessionairesService.getEmptyConcessionaire();
        } else {
            vm.concessionaire = angular.copy(Concessionaire); // Copiamos para no modificar el original hasta guardar
        }

        // Methods
        vm.saveConcessionaire = saveConcessionaire;
        vm.closeDialog = closeDialog;
        vm.addSource = addSource;
        vm.removeSource = removeSource;
        vm.getOrigins = getOrigins;
        vm.getChannels = getChannels;

        //////////
        /**
         * Guardar concessionaireo
         */
        function saveConcessionaire() {
            var c=angular.copy(vm.concessionaire);
            //lo borramos porque ya lo editamos en otro dialogo
            delete vm.concessionaire.work_calendar;
            return concessionairesService.saveConcessionaire(c).then(function(){
                NotifyService.successMessage(gettextCatalog.getString("Concesionario guardado correctamente"));
                closeDialog();
            }, function(error){
                vm.serverErrors = error.data;
                NotifyService.errorMessage(gettextCatalog.getString("Error al guardar el concesionario.") +" "+ (error.data.non_field_errors || ""));
            });
        }

        /**
         * Cerrar el cuadro de diálogo sin cambios
         */
        function closeDialog() {
            $mdDialog.hide();
        }

        /**
         * Añade un source
         */
        function addSource() {
            vm.concessionaire.sources.push({data:""});
        }

        /**
         * Borra un source
         */
        function removeSource($index,form, item) {
            if(item.id){
                return concessionairesService.removeSource(angular.copy(item)).then(function(){
                    form.$setDirty();
                    vm.concessionaire.sources.splice($index,1);
                }, function(error){
                    NotifyService.errorMessage(gettextCatalog.getString("Error al borrar la fuente.") +" "+ (error.data.non_field_errors || ""));
                });
            }else{
                form.$setDirty();
                vm.concessionaire.sources.splice($index,1);
            }
        }

        /* Orígenes */
        function getOrigins(searchText) {
            var deferred = $q.defer();
            originsService.getAllOrigins(searchText).then(function(origins){
                deferred.resolve(origins);
            });
            return deferred.promise;
        }

        /* Canales */
        function getChannels(searchText,origin) {
            var deferred = $q.defer();
            //Primero comprobamos si el origen seleccionado tiene algun canal, si lo tiene devolvemos esos canales, si no devolvemos todos los canales
            if(origin.available_channels_data.length>0){
                deferred.resolve(origin.available_channels_data);
            }else{
                channelsService.getAllChannels(searchText).then(function(channels){
                    deferred.resolve(channels);
                });
            }
            return deferred.promise;
        }

    }
})();
