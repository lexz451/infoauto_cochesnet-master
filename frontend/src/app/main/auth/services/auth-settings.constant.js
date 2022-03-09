(function()
{
    'use strict';

    angular
        .module('app.auth')
        .constant('authSettings', {

            /**
             * estado ($route) al que se cambiará cuando sea necesario pedir el login de usuario
             */
            LOGIN_STATE: 'app.auth.login',

            /**
             * estado ($route) al que se cambiará cuando el logueo sea correcto
             */
            LOGIN_STATE_SUCCESS: 'app.leads.board',

            /**
             * evento que se emitirá mediante $rootScope.broadcast() cuando el usuario se identifique correctamente. Si
             * es un valor que se evalúe como false, no se emitirá ningún evento
             */
            ON_LOGIN_BROADCAST: 'auth.login',

            /**
             * evento que se emitirá mediante $rootScope.broadcast() cuando el usuario cierra la sesión. Si
             * es un valor que se evalúe como false, no se emitirá ningún evento
             */
            ON_LOGOUT_BROADCAST: 'auth.logout',

            /**
             * evento que se emitirá mediante $rootScope.broadcast() cuando el usuario hace alguna petición
             * que devuelve un 401 o 403. Si es un valor que se evalúe como false, no se emitirá ningún evento
             */
            ON_UNAUTHORIZED_REQUEST: 'auth.unauthorized'

        } );

})();
