(function () {
    'use strict';

    angular
        .module('app.tasks')
        .factory('tasksService', tasksService);

    /** @ngInject */
    function tasksService($q, api) {

        var service = {
            tasks: {
                data: [],
                count: 0,
                filters: {}
            },
            getTasks: getTasks,
            getAllTasks: getAllTasks,
            getTask: getTask,
            saveTask: saveTask,
            getEmptyTask: getEmptyTask,
            removeTask: removeTask
        };

        return service;

        //////////

        /**
         * Obtiene el listado de tasks
         */
        function getTasks() {
            // Create a new deferred object
            var deferred = $q.defer();
            
            api.tasks.get(service.tasks.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                service.tasks.data = response.results;
                service.tasks.count = response.count;

                deferred.resolve(service.tasks);
            }

            function getKO(response) {
                //con esto evitamos que den problemas los not found cuando
                // filtramos y estamos en una página que ya no existe
                if(response.status==404 && service.tasks.filters.page!=1){
                    service.tasks.filters.page=1;
                }
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de tasks filtrando unicamente por el texto dado y sin guardar en el servicio
         *
         * @param search
         */
        function getAllTasks(search) {
            // Create a new deferred object
            var deferred = $q.defer();
            var f=angular.copy(service.tasks.filters);
            f.search=search;
            f.page_size="all";
            api.tasks.get(f, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene los datos de una task determinado por su ID
         *
         * @param id
         */
        function getTask(id) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.tasks.get({id: id}, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Guarda la task que se pasa como parámetro. Si ya existe actualiza el existente.
         *
         * @param form
         */
        function saveTask(form) {
            var deferred = $q.defer();

            var task=angular.copy(form);

            if (form.id) {
                api.tasks.update(task, updateOK, saveKO);
            } else {
                api.tasks.create(task, createOK, saveKO);
            }

            return deferred.promise;


            function createOK(response) {
                // Store the tasks
                service.tasks.data.push(response);
                service.tasks.count ++;
                deferred.resolve(response);
            }

            function updateOK(response) {
                // Actauliza el listado
                for (var i = 0; i < service.tasks.data.length; i++) {
                    if (service.tasks.data[i].id === response.id) {
                        service.tasks.data[i] = angular.copy(response);
                    }
                }
                deferred.resolve(response);
            }

            function saveKO(response) {
                deferred.reject(response);
            }

        }

        /**
         * Devuelve un task vacío
         */
        function getEmptyTask(lead, request, tracing) {
            return {
                request:[request.id],
                lead:lead,
                media:'Phone',
                is_traking_task: tracing,
                note:[]
            };
        }
        
        function removeTask(task){
            var deferred = $q.defer();

            api.tasks.remove({id: task.id}, taskRemoveOK, removeKO);

            // Task borrado correctamente
            function taskRemoveOK(response){
                // Quitamos la task en los datos locales
                for (var i = 0; i < service.tasks.data.length; i++) {
                    if (service.tasks.data[i].id === task.id) {
                        service.tasks.data.splice(i,1);
                        service.tasks.count -= 1;
                        break;
                    }
                }
                deferred.resolve(response.data);
            }

            // Fallo al borrar task
            function removeKO(response){
                deferred.reject(response);
            }

            return deferred.promise;
        }

    }

})();
