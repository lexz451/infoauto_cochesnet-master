(function () {
    'use strict';

    angular
        .module('app.users')
        .factory('usersService', usersService);

    /** @ngInject */
    function usersService($q, api) {

        var service = {
            users: {
                data: [],
                count: 0,
                filters: {}
            },
            getUsers: getUsers,
            getAllUsers: getAllUsers,
            getAllUsersConcessionaire: getAllUsersConcessionaire,
            getAllAdmins: getAllAdmins,
            getUser: getUser,
            saveUser: saveUser,
            getEmptyUser: getEmptyUser,
            removeUser: removeUser,
            removeConcessionaire: removeConcessionaire,
            removeSFA: removeSFA
        };

        return service;

        //////////

        /**
         * Obtiene el listado de users
         */
        function getUsers() {
            // Create a new deferred object
            var deferred = $q.defer();

            var f=angular.copy(service.users.filters);

            if(f.concessionaire_data && f.concessionaire_data.id){
                f.userconcession__concessionaire__id=f.concessionaire_data.id;
            }

            delete f.concessionaire_data;

            api.users.get(f, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                service.users.data=response.results;
                service.users.count = response.count;

                deferred.resolve(service.users);
            }

            function getKO(response) {
                //con esto evitamos que den problemas los not found cuando
                // filtramos y estamos en una página que ya no existe
                if(response.status==404 && service.users.filters.page!=1){
                    service.users.filters.page=1;
                    getUsers();
                }
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de users filtrando unicamente por el texto dado y sin guardar en el servicio
         *
         * @param search
         */
        function getAllUsers(search) {
            // Create a new deferred object
            var deferred = $q.defer();
            var f=angular.copy(service.users.filters);
            f.search=search;
            f.page_size="all";
            api.users.get(f, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de users filtrando unicamente por el texto dado y sin guardar en el servicio
         *
         * @param search
         */
        function getAllUsersConcessionaire(search, Concessionaire) {
            // Create a new deferred object
            var deferred = $q.defer();
            var f={};
            f.userconcession__concessionaire__id=Concessionaire;
            f.search=search;
            f.page_size="all";
            api.users.get(f, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de administradores filtrando unicamente por el texto dado y sin guardar en el servicio
         *
         * @param search
         */
        function getAllAdmins(search, concessionaire) {
            // Create a new deferred object
            var deferred = $q.defer();
            var f=angular.copy(service.users.filters);
            f.search=search;
            f.concessionaire=concessionaire.id;
            f.page_size="all";
            api.admins.get(f, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene los datos de una user determinado por su ID
         *
         * @param id
         */
        function getUser(id) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.users.get({id: id}, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Guarda la user que se pasa como parámetro. Si ya existe actualiza el existente.
         *
         * @param form
         */
        function saveUser(form) {
            var deferred = $q.defer();

            var user = angular.copy(form);

            for(var i in user.related_concessionaires){
                if(user.related_concessionaires[i].concessionaire_data && user.related_concessionaires[i].concessionaire_data.id){
                    user.related_concessionaires[i].concessionaire=user.related_concessionaires[i].concessionaire_data.id;
                }
            }

            if(form.id){
                api.users.update(user, updateOK, saveKO);
            }else{
                api.users.create(user, createOK, saveKO);
            }

            return deferred.promise;


            function createOK(response) {
                service.getUsers();
                deferred.resolve(response);
            }

            function updateOK(response) {
                // Actauliza el listado
                for (var i = 0; i < service.users.data.length; i++) {
                    if (service.users.data[i].id === response.id) {
                        service.users.data[i] = angular.copy(response);
                    }
                }
                deferred.resolve(response);
            }

            function saveKO(response) {
                deferred.reject(response);
            }

        }

        /**
         * Devuelve un usero vacío
         */
        function getEmptyUser() {
            return {
                related_concessionaires:[]
            };
        }
        
        function removeUser(user){
            var deferred = $q.defer();

            api.users.remove({id: user.id}, userRemoveOK, removeKO);

            // Usero borrado correctamente
            function userRemoveOK(response){
                // Quitamos la user en los datos locales
                for (var i = 0; i < service.users.data.length; i++) {
                    if (service.users.data[i].id === user.id) {
                        service.users.data.splice(i,1);
                        service.users.count -= 1;
                        break;
                    }
                }
                deferred.resolve(response.data);
            }

            // Fallo al borrar centro
            function removeKO(response){
                deferred.reject(response);
            }

            return deferred.promise;
        }

        function removeConcessionaire(item){
            var deferred = $q.defer();

            api.users.removeConcessionaire({id: item.id}, userRemoveOK, removeKO);

            // borrado correctamente
            function userRemoveOK(response){
                deferred.resolve(response.data);
            }

            // Fallo al borrar
            function removeKO(response){
                deferred.reject(response);
            }

            return deferred.promise;
        }

        function removeSFA(item){
            var deferred = $q.defer();

            api.users.removeSFA({id: item.id}, userRemoveOK, removeKO);

            // borrado correctamente
            function userRemoveOK(response){
                deferred.resolve(response.data);
            }

            // Fallo al borrar
            function removeKO(response){
                deferred.reject(response);
            }

            return deferred.promise;
        }
        

    }

})();
