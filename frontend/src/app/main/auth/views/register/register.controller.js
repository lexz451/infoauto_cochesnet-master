(function ()
{
    'use strict';

    angular
        .module('app.auth')
        .controller('RegisterController', RegisterController);

    /** @ngInject */
    function RegisterController(AuthService, NotifyService, $q, gettextCatalog)
    {
        var vm = this;
        // Data
        vm.form = {};


        // Methods
        vm.register = register;

        //////////

        /*
        * Registro de empresa
        * */
        function register(){
            var form=angular.copy(vm.form);
            return AuthService.register(form).then(function(data){
                // $state.go("app.auth.login");
                NotifyService.successMessage(gettextCatalog.getString("Registro realizado correctamente"));
            }, function(error){
                vm.serverErrors = error.data;
                NotifyService.errorMessage(gettextCatalog.getString("Error al realizar el registro"));
            });
        }

    }
})();