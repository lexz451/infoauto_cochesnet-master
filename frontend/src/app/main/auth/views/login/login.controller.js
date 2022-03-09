(function ()
{
    'use strict';

    angular
        .module('app.auth')
        .controller('LoginController', LoginController);

    /** @ngInject */
    function LoginController(AuthService, NotifyService, $stateParams)
    {
        var vm = this;
        // Data

        // Methods
        vm.login = login;
        vm.loginSelected=$stateParams.action || "students";

        //////////
        function login(){
            return AuthService.login(vm.username, vm.password).then(function(user){
                //console.log("OK")
                //se ejecutará el evento por broadcast
            }, function(res){
                NotifyService.errorMessage(res.error);
            });
        }
    }
})();