(function ()
{
    'use strict';

    angular
        .module('app.utils.debounce')
        .factory("DebounceService", DebounceService);


    /** @ngInject */
    function DebounceService ( $timeout, $rootScope ) {

        return debounce;

        /////////////

        /**
         * Muestra un mensaje simple de error
         */
        function debounce (callback, interval) {
            var timeout = null;
            return function(o,n) {
                //solo aplicamos esto si realmente cambian los filtros
                if(o!==n){
                    $rootScope.loadingProgress = true;
                    $timeout.cancel(timeout);
                    timeout = $timeout(function () {
                        callback.apply(this, arguments).then(function(){
                            $rootScope.loadingProgress = false;
                        });
                    }, interval);
                }
            };
        }
    }

})();
