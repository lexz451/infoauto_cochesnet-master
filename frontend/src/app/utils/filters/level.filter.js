
(function () {
    'use strict';

    angular
        .module('app.utils.filters')
        .filter('level', level);

    function level(gettextCatalog) {
        return function(input) {
            if(input==="initial"){
                return gettextCatalog.getString("Inicial");
            }
            if(input==="medium"){
                return gettextCatalog.getString("Medio");
            }
            if(input==="advanced"){
                return gettextCatalog.getString("Avanzado");
            }
            return input;
        }
    }
})();
