(function () {
    'use strict';

    angular
        .module('app.concessionaires')
        .controller('ConcessionaireNotesDialogController', ConcessionaireNotesDialogController);

    /** @ngInject */
    function ConcessionaireNotesDialogController($mdDialog, Concessionaire, concessionairesService, NotifyService, originsService, channelsService, $q, gettextCatalog) {
        var vm = this;

        // Data
        vm.title = gettextCatalog.getString('Notas');

        vm.concessionaire = angular.copy(Concessionaire); // Copiamos para no modificar el original hasta guardar

        // Methods
        vm.saveConcessionaire = saveConcessionaire;
        vm.addNote = addNote;
        vm.deleteNote = deleteNote;
        vm.closeDialog = closeDialog;

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
         * Añade una nota
         */
        function addNote(){
            vm.concessionaire.notes_data.push({content:'', modified:new Date()});
        }

        /**
         * borra una nota
         */
        function deleteNote(note){
            if(note.id){
                //buscamos por id
                for (var i = 0; i < vm.concessionaire.notes_data.length; i++) {
                    if (vm.concessionaire.notes_data[i].id === note.id) {
                        vm.concessionaire.notes_data.splice(i,1);
                        break;
                    }
                }
            }else{
                //buscamos por contenido
                for (var i = 0; i < vm.concessionaire.notes_data.length; i++) {
                    if (vm.concessionaire.notes_data[i].content === note.content && !note.id) {
                        vm.concessionaire.notes_data.splice(i,1);
                        break;
                    }
                }
            }
        }

        /**
         * Cerrar el cuadro de diálogo sin cambios
         */
        function closeDialog() {
            $mdDialog.hide();
        }

    }
})();
