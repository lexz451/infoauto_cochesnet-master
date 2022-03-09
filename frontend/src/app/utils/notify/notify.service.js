(function ()
{
    'use strict';

    angular
        .module('app.utils.notify')
        .factory("NotifyService", NotifyService);


    /** @ngInject */
    function NotifyService ( $mdToast ) {
        var service = {
            errorMessage: showErrorMessage,
            successMessage: showSuccessMessage
        };

        return service;

        /////////////

        /**
         * Muestra un mensaje simple de error
         */
        function showErrorMessage ( message )
        {
            //Damos mas tiempo a lo mensajes mas largos
            var time=2500;
            time+=(message.length*20);
            $mdToast.show(
                $mdToast.simple()
                    .textContent(message)
                    .theme('toast-error')
                    .hideDelay(time)
            );
        }

        /**
         * Muestra un mensaje simple de éxito
         */
        function showSuccessMessage ( message )
        {
            //Damos mas tiempo a lo mensajes mas largos
            var time=2500;
            time+=(message.length*20);
            $mdToast.show(
                $mdToast.simple()
                    .textContent(message)
                    .theme('toast-success')
                    .hideDelay(time)
            );
        }



    }

})();
