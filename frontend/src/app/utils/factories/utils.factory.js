
(function () {
    'use strict';

    angular
        .module('app.utils.factory', [])
        .factory('utils', utils);

    function utils(localStorageService, DebounceService, $state) {
        return  {
            filtersAndOrdering : function(scope, vm, itemOrdering, service, filtered){
                vm.ordering = localStorageService.get(itemOrdering);
                scope.$watchCollection('vm.ordering', function (newValue, oldValue) {
                    if(newValue !== oldValue) {
                        if(vm.ordering !== undefined){
                            localStorageService.set(itemOrdering, vm.ordering);
                        }
                        if (filtered){
                            DebounceService(service.listFiltered, 300)();
                        }else{
                            DebounceService(service.list, 300)();
                        }
                    }
                });

                // Cambios en el número de páginas
                scope.$watch('config.itemsPerPage', function (newValue, oldValue) {
                    if (newValue !== oldValue){
                        if (filtered){
                            DebounceService(service.listFiltered, 300)();
                        }else{
                            DebounceService(service.list, 300)();
                        }
                    }
                });
            }
        }
    }
})();
