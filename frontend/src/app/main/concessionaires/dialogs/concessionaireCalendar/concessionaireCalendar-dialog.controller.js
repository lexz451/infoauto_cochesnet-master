(function () {
    'use strict';

    angular
        .module('app.concessionaires')
        .controller('ConcessionaireCalendarDialogController', ConcessionaireCalendarDialogController);

    /** @ngInject */
    function ConcessionaireCalendarDialogController($mdDialog, Concessionaire, concessionairesService, NotifyService, originsService, channelsService, $q, gettextCatalog) {
        var vm = this;

        // Data
        vm.title = gettextCatalog.getString('Calendario de trabajo');

        vm.concessionaire = angular.copy(Concessionaire); // Copiamos para no modificar el original hasta guardar

        vm.week={};
        vm.week.monday=gettextCatalog.getString("Lunes");
        vm.week.tuesday=gettextCatalog.getString("Martes");
        vm.week.wednesday=gettextCatalog.getString("Miércoles");
        vm.week.thursday=gettextCatalog.getString("Jueves");
        vm.week.friday=gettextCatalog.getString("Viernes");
        vm.week.saturday=gettextCatalog.getString("Sábado");
        vm.week.sunday=gettextCatalog.getString("Domingo");

        init();

        // Methods
        vm.saveConcessionaire = saveConcessionaire;
        vm.closeDialog = closeDialog;

        //////////
        function init(){
            if(!vm.concessionaire.work_calendar){
                vm.concessionaire.work_calendar={};
                vm.concessionaire.work_calendar.monday={
                    working_day:false
                };
                vm.concessionaire.work_calendar.tuesday={
                    working_day:false
                };
                vm.concessionaire.work_calendar.wednesday={
                    working_day:false
                };
                vm.concessionaire.work_calendar.thursday={
                    working_day:false
                };
                vm.concessionaire.work_calendar.friday={
                    working_day:false
                };
                vm.concessionaire.work_calendar.saturday={
                    working_day:false
                };
                vm.concessionaire.work_calendar.sunday={
                    working_day:false
                };
            }else{
                var c=vm.concessionaire;
                for(var i in c.work_calendar){
                    if(c.work_calendar[i].start_hour){
                        c.work_calendar[i].start_hour=moment(c.work_calendar[i].start_hour,"HH:mm").toDate();
                    }
                    if(c.work_calendar[i].end_hour){
                        c.work_calendar[i].end_hour=moment(c.work_calendar[i].end_hour,"HH:mm").toDate();
                    }
                }
            }
        }

        /**
         * Guardar concessionaireo
         */
        function saveConcessionaire() {
            var c=angular.copy(vm.concessionaire);
            for(var i in c.work_calendar){
                if(c.work_calendar[i].start_hour){
                    c.work_calendar[i].start_hour=moment(c.work_calendar[i].start_hour).format("HH:mm");
                }
                if(c.work_calendar[i].end_hour){
                    c.work_calendar[i].end_hour=moment(c.work_calendar[i].end_hour).format("HH:mm");
                }
            }
            return concessionairesService.saveConcessionaire(c).then(function(){
                NotifyService.successMessage(gettextCatalog.getString("Calendario guardado correctamente"));
                closeDialog();
            }, function(error){
                vm.serverErrors = error.data;
                NotifyService.errorMessage(gettextCatalog.getString("Error al guardar el calendario.") +" " + (error.data.non_field_errors || ""));
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
