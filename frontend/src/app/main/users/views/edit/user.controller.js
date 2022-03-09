(function () {
    'use strict';

    angular
        .module('app.users')
        .controller('UserEditController', UserEditController);

    /** @ngInject */
    function UserEditController(currentUser, User, usersService, $rootScope, NotifyService, $state, gettextCatalog, api,
                                Schools, Courses, Specialities, schoolsService, $q) {
        var vm = this;

        // Data
        vm.user=User;
        vm.schools=Schools;
        vm.courses=Courses;
        vm.specialities=Specialities;

        //Preparación de opciones para la subida de la imagen de perfil
        vm.ngFlowOptions={
            target: api.URLs.users.replace(":id",vm.user.id),
            uploadMethod: "PATCH",
            fileParameterName: "image"
        };

        init();

        // Methods
        vm.saveUser = saveUser;
        vm.removeImage = removeImage;
        vm.imageError = imageError;
        vm.reloadImage = reloadImage;
        vm.getSchools = getSchools;

        //////////
        function init(){
            if(vm.user.hire_date){
                vm.user.hire_date=moment(vm.user.hire_date,"DD/MM/YYYY").toDate();
            }else{
                vm.user.hire_date=null;
            }
            if(vm.user.born_date){
                vm.user.born_date=moment(vm.user.born_date,"DD/MM/YYYY").toDate();
            }else{
                vm.user.born_date=null;
            }
        }

        /**
         * Guardar detalle del usuario
         */
        function saveUser(user) {
            var form=angular.copy(user);

            return usersService.saveUser(form).then(function(response){
                $state.go("app.users.get.edit",{user:response.id});
                vm.user.image=response.image;
                NotifyService.successMessage(gettextCatalog.getString("Cambios realizados correctamente"));
            }, function(error){
                vm.serverErrors = error.data;
                NotifyService.errorMessage(gettextCatalog.getString("Error al guardar los datos básicos.") +" "+ (error.data.non_field_errors || ""));
            });
        }

        function removeImage(){
            saveUser({image:null,id:vm.user.id});
        }

        /* Error al subir imagen */
        function imageError($file, $message, $flow) {
            $file.cancel();
            vm.serverErrors=JSON.parse($message);
            var msg="";
            if(vm.serverErrors.image && vm.serverErrors.image[0]){
                msg+=vm.serverErrors.image[0];
            }
            NotifyService.errorMessage(gettextCatalog.getString("Error al modificar foto. ")+msg);
        }

        /* Recarga de imagen */
        function reloadImage(file, response, flow) {
            var res=JSON.parse(response);
            vm.user.image=res.image;
            NotifyService.successMessage(gettextCatalog.getString("Foto modificada correctamente"));
        }

        /* Escuelas */
        function getSchools(searchText) {
            var deferred = $q.defer();
            schoolsService.schools.filters={};
            // schoolsService.getAllSchools(searchText).then(function(schools){
            schoolsService.getSchools(searchText).then(function(schools){
                // deferred.resolve(schools);
                deferred.resolve(schools.data);
            });
            return deferred.promise;
        }

    }
})();
