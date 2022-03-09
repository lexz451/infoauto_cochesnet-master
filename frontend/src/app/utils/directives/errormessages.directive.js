(function () {
    'use strict';

    angular
        .module('app.utils.directives')
        .controller('ErrorMessagesController', ErrorMessagesController)
        .directive('errorMessages', errorMessagesDirective);

    /** @ngInject */
    function ErrorMessagesController($attrs, $scope, $timeout, gettextCatalog) {
        var vm = this;
        vm.messages = [];
        vm.serverMessages = [];

        init();

        function init() {
            // Atributo required
            if (angular.isDefined($attrs.required)) {
                vm.messages.push({
                    type: ['required'],
                    message: gettextCatalog.getString('Este campo es obligatorio')
                });
            }

            if (angular.isDefined($attrs.mdRequireMatch)) {
                vm.messages.push({
                    type: ['md-require-match'],
                    message: gettextCatalog.getString('Debe seleccionar una opción de la lista')
                });
            }

            if (angular.isDefined($attrs.url)){
                vm.messages.push({
                    type: ['url'],
                    message: gettextCatalog.getString("La dirección web debe ser de la forma http://...")
                });
            }

            // Atributo pattern
            if (angular.isDefined($attrs.pattern)) {
                vm.messages.push({
                    type: ['pattern'],
                    message: gettextCatalog.getString($attrs.pattern)
                });
            }

            // Atributo match-password
            if (angular.isDefined($attrs.passwordMatch)) {
                vm.messages.push({
                    type: ['passwordMatch'],
                    message: gettextCatalog.getString("Las contraseñas no coinciden")
                });
            }

            // Atributo match-password
            if (angular.isDefined($attrs.unique)) {
                vm.messages.push({
                    type: ['unique'],
                    message: gettextCatalog.getString("El email indicado ya existe")
                });
            }
        }

        function getValueObject(obj,keys) {
            var o=obj;
            for(var i in keys){
                o=o[keys[i]];
                if(!o){
                    return false;
                }
            }
            return o[0];
        }

        $scope.$watch("ErrorMessages.errors", function () {
            vm.serverMessages.length = 0;
            if(vm.field && vm.field.$name && vm.errors){
                var parents=vm.field.$name.split("___");
                var message=getValueObject(vm.errors,parents);

                if(message){
                    vm.serverMessages.push(message);
                    vm.field.$setTouched();
                    vm.field.$setValidity("serverError", false);
                    if (angular.isDefined($attrs.forcechange)) {
                        $timeout(function(){
                            vm.field.$setValidity("serverError", true);
                        },6000);
                    }
                }
            }
        });

    }

    /** @ngInject */
    function errorMessagesDirective($timeout) {
        return {
            restrict: 'E',
            scope: {},
            replace: true,
            bindToController: {
                field: '=field',
                errors: '=serverErrors'
            },
            controller: 'ErrorMessagesController as ErrorMessages',
            template: '<div ng-messages="ErrorMessages.field.$error" ng-show="ErrorMessages.field.$touched || ErrorMessages.serverMessages.length > 0" role="alert"><div ng-hide="ErrorMessages.serverMessages.length > 0" ng-repeat="message in ErrorMessages.messages" ng-message-exp="message.type"><span>{{message.message}}</span></div><div ng-repeat="message in ErrorMessages.serverMessages" ng-message="serverError" class="has-animate"><span>{{message}}</span></div></div>',
            link: function (scope, iElement) {
                $timeout(function(){
                    var animate=$(iElement).find(".has-animate");
                    if(animate){
                        if(!animate.hasClass("ng-animate")){
                            animate.addClass("ng-animate");
                        }
                    }
                });
            }
        };
    }
})();
