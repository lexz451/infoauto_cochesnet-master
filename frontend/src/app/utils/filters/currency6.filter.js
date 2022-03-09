(function () {
    'use strict';

    angular
        .module('app.utils.filters')
        .filter('currency6', currency6);

    function currency6(currencyFilter) {
        return function(amount){
            return currencyFilter(amount,'€',6);
        }
    }
})();
