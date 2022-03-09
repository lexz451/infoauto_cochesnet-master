(function () {
    'use strict';

    angular
        .module('app.utils.directives')
        .controller('ParametersController', ParametersController)
        .directive('parameters', parametersDirective);

    /** @ngInject */
    function ParametersController($timeout) {
        var vm = this;

        vm.selectedParameter=null;
        vm.breadcrumb=[];
        vm.load=false;

        // Methods
        vm.addToBreadcrumb = addToBreadcrumb;
        vm.addValueParemeter = addValueParemeter;
        vm.resetParameters = resetParameters;
        vm.showMenu = showMenu;
        vm.notEmpty = notEmpty;

        //////////

        /**
         * Añade al breadcrumb el rastro de migas
         */
        function addToBreadcrumb(key, obj) {
            vm.load=true;
            $timeout(function(){
                vm.load=false;
            },500);
            //si tiene key se entiende que es un paso hacia adelante
            if(key){
                vm.selectedParameter=obj.data || obj;
                vm.breadcrumb.push({
                    "key":key,
                    "value":obj.human_name,
                    "parameters":obj.data || obj
                });
            }else{
                //Si no tiene key es que quiere ir al padre
                vm.breadcrumb.splice(-1,1);
                if(vm.breadcrumb.length){
                    vm.selectedParameter=vm.breadcrumb[vm.breadcrumb.length-1].parameters;
                }else{
                    vm.selectedParameter=null;
                }
            }
        }

        /**
         * Añade al campo de texto la variable que hayamos indicado
         */
        function addValueParemeter(key) {
            var s="";
            for(var i in vm.breadcrumb){
                s+=vm.breadcrumb[i].key+".";
            }
            s+=key;
            if(typeof vm.model==="string"){
                vm.model+=" "+s+" ";
            }
            else if(typeof vm.model==="object"){
                if(vm.model.indexOf(s)===-1){
                    vm.model.push(s);
                }
            }
            resetParameters();
        }

        function resetParameters(){
            vm.selectedParameter=null;
            vm.breadcrumb=[];
        }

        function showMenu(params){
            for(var i in params){
                if(notEmpty(params[i][vm.filter])){
                    return true;
                }
            }
            return false;
        }

        function notEmpty(obj){
            return Object.keys(obj).length>0;
        }


    }

    /** @ngInject */
    function parametersDirective() {
        return {
            restrict: 'E',
            scope: {},
            bindToController: {
                model: '=model',
                filter: '=filter',
                parameters: '=parameters',
                icon: '@icon'
            },
            controller: 'ParametersController as Parameters',
            templateUrl: 'app/main/parameters/parameters.html',
            link: function (scope, iElement) {

            }
        };
    }
})();
