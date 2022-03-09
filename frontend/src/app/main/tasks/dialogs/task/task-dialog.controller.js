(function () {
    'use strict';

    angular
        .module('app.tasks')
        .controller('TaskDialogController', TaskDialogController);

    /** @ngInject */
    function TaskDialogController($mdDialog, Task, Request, Lead, Tracing, tasksService, NotifyService, taskTypesService, usersService,
                                  originsCarService, GasTypes, $q, gettextCatalog) {
        var vm = this;

        // Data
        vm.title = gettextCatalog.getString('Editar tarea');
        vm.taskTypes=[];
        vm.origins=originsCarService.origins;
        vm.gasTypes=GasTypes;
        vm.now=new Date();

        if (!Task) {
            vm.title = gettextCatalog.getString('Nueva tarea');
            vm.task = tasksService.getEmptyTask(Lead, Request, Tracing);
        } else {
            vm.task = angular.copy(Task); // Copiamos para no modificar el original hasta guardar
        }
        init();


        // Methods
        vm.saveTask = saveTask;
        vm.addTaskNote = addTaskNote;
        vm.deleteTaskNote = deleteTaskNote;
        vm.closeDialog = closeDialog;

        //////////
        function init() {
            taskTypesService.getTaskTypes(Tracing).then(function(res){
                vm.taskTypes=res;
            });

            vm.task.date=vm.task.date ? new Date(moment(vm.task.date).format()) : null;
            vm.task.planified_realization_date=vm.task.planified_realization_date ? new Date(moment(vm.task.planified_realization_date).format()) : null;
            vm.task.realization_date=vm.task.realization_date ? new Date(moment(vm.task.realization_date).format()) : null;
            vm.task.planified_tracking_date=vm.task.planified_tracking_date ? new Date(moment(vm.task.planified_tracking_date).format()) : null;
            vm.task.tracking_date=vm.task.tracking_date ? new Date(moment(vm.task.tracking_date).format()) : null;
        }

        /**
         * Guardar informe
         */
        function saveTask() {

            if(vm.task.planified_realization_date)
                vm.task.planified_realization_date.setHours(vm.task.datetime.getHours(),vm.task.datetime.getMinutes())

            if(Request.id){
                return tasksService.saveTask(angular.copy(vm.task)).then(function(res){
                    NotifyService.successMessage(gettextCatalog.getString("Solicitud guardada correctamente"));
                    closeDialog();
                    if(!vm.task.id){
                        Request.task.push(vm.task);
                    }
                }, function(error){
                    vm.serverErrors = error.data;
                    NotifyService.errorMessage(gettextCatalog.getString("Error al guardar la solicitud.") +" "+ (error.data.non_field_errors || ""));
                });
            }else{
                if(!Task){
                    // vm.task.planified_realization_date.setHours(vm.task.datetime.getHours(),vm.task.datetime.getMinutes())
                    Request.task.push(vm.task);
                    tasksService.tasks.data.push(vm.task);
                    tasksService.tasks.count++;
                }else{
                    for(var i in vm.task){
                        Task[i]=vm.task[i];
                    }
                }
                closeDialog();
            }
        }

        /**
         * Añade una nota a la tarea
         */
        function addTaskNote(task){
            vm.task.note.push({content: '', essential: false, modified:new Date()});
        }

        /**
         * borra una nota de la tarea
         */
        function deleteTaskNote(note){
            if (note.id) {
                //buscamos por id
                for (var i = 0; i < vm.task.note.length; i++) {
                    if (vm.task.note[i].id === note.id) {
                        vm.task.note.splice(i, 1);
                        break;
                    }
                }
            } else {
                //buscamos por contenido
                for (var i = 0; i < vm.task.note.length; i++) {
                    if (vm.task.note[i].content === note.content && !note.id) {
                        vm.task.note.splice(i, 1);
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
