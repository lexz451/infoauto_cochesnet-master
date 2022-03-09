(function ()
{
    'use strict';
    angular
        .module('app.users')
        .controller('UsersController', UsersController);
    /** @ngInject */
    function UsersController($scope, currentUser, usersService, Users, NotifyService, $rootScope, DebounceService,
                             leadsService, Concessionaire, $mdDialog, $document, concessionairesService, $q, gettextCatalog)
    {
        var vm = this;
        // Data
        vm.user = currentUser;
        vm.users=Users;

        // Watchers
        $scope.$watch('vm.users.filters', DebounceService(usersService.getUsers, 300), true);

        // Methods
        vm.openUserDialog = openUserDialog;
        vm.removeUser = removeUser;
        vm.getConcessionaires = getConcessionaires;
        vm.toggleActive = toggleActive;

        //////////
        /**
         * Abre el dialogo para crear/editar una user
         *
         * @param ev
         * @param user
         */
        function openUserDialog(ev, user) {
            $mdDialog.show({
                controller: 'UserDialogController',
                controllerAs: 'vm',
                templateUrl: 'app/main/users/dialogs/user/user-dialog.html',
                parent: angular.element($document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                locals: {
                    User:user,
                    event: ev
                }
            });
        }

      
        /**
         * Abre el dialogo para eliminar una user
         *
         * @param ev
         * @param user
         */
        function removeUser(ev, user) {
            var confirm = $mdDialog.confirm()
                .title(gettextCatalog.getString('Eliminar concesionario')+' "'+user.name+'"')
                .textContent(gettextCatalog.getString('¿Seguro que quieres eliminar el concesionario?'))
                .ariaLabel(gettextCatalog.getString('Eliminar concesionario'))
                .clickOutsideToClose(true)
                .parent(angular.element(document.body))
                .ok(gettextCatalog.getString('Borrar concesionario'))
                .cancel(gettextCatalog.getString('Cancelar'));

            $mdDialog.show(confirm).then(function() {
                usersService.removeUser(user).then(function(){
                    NotifyService.successMessage(gettextCatalog.getString("Concesionario borrado correctamente."));
                }, function(error){
                    NotifyService.errorMessage("Error al borrar el concesionario." +" "+ (error.data.detail || ""));
                });
            });

        }

        /* Concesionarios */
        function getConcessionaires(searchText) {
            var deferred = $q.defer();
            /*phonesService.getAllPhones(searchText).then(function(concessionaires){
                deferred.resolve(concessionaires);
            });*/
            concessionairesService.getAllConcessionaires(searchText).then(function(concessionaires){
                deferred.resolve(concessionaires);
            });

            return deferred.promise;
        }

        /* toggle */
        function toggleActive(user) {
            var deferred = $q.defer();
            //Comprobamos que tenemos permiso para realizar esta acción
            if(vm.user.is_concession_admin){
                for(var i in user.related_concessionaires){
                    var sw=existConcessionaire(user.related_concessionaires[i].concessionaire, vm.user.related_concessionaires);
                    if(!sw){
                        NotifyService.errorMessage(gettextCatalog.getString("No eres competente para realizar esta acción. Por favor contacte con atención al cliente."));
                        deferred.resolve(false);
                        return deferred.promise;
                    }
                }
            }

            //Una vez que tenemos permiso comprobamos si hay leads para modificar su asiganación
            leadsService.getLeadsByUser(user.id).then(function (res) {
                if(res.count){
                    //abrimos modal
                    openLeadByUserDialog(user);
                    deferred.resolve(true);
                }else{
                    //realizamos la baja/alta
                    var obj={
                        id:user.id,
                        is_active:!user.is_active
                    };
                    return usersService.saveUser(obj).then(function(res){
                        if(res.is_active){
                            NotifyService.successMessage(gettextCatalog.getString("Usuario dado de alta correctamente"));
                        }else{
                            NotifyService.successMessage(gettextCatalog.getString("Usuario dado de baja correctamente"));
                        }
                        deferred.resolve(true);
                    }, function(error){
                        vm.serverErrors = error.data;
                        if(obj.is_active){
                            NotifyService.errorMessage(gettextCatalog.getString("Error al dar de alta a este usuario.") +" "+ (error.data.non_field_errors || ""));
                        }else{
                            NotifyService.errorMessage(gettextCatalog.getString("Error al dar de baja a este usuario.") +" "+ (error.data.non_field_errors || ""));
                        }
                        deferred.resolve(false);
                    });
                }
            },function(){
                NotifyService.errorMessage(gettextCatalog.getString("Se ha producido un error."));
                deferred.resolve(false);
            });

            return deferred.promise;
        }

        function existConcessionaire(id,concessionaires){
            for(var j in vm.user.related_concessionaires){
                if(id===concessionaires[j].concessionaire){
                    return true;
                }
            }
            return false;
        }

        /**
         * Abre el dialogo para crear/editar una user
         */
        function openLeadByUserDialog(user) {
            $mdDialog.show({
                controller: 'LeadByUserDialogController',
                controllerAs: 'vm',
                templateUrl: 'app/main/users/dialogs/leadByUser/leadByUser-dialog.html',
                parent: angular.element($document.body),
                clickOutsideToClose: true,
                locals: {
                    User:user
                }
            });
        }

    }
})();