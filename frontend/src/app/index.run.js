(function ()
{
    'use strict';

    angular
        .module('fuse')
        .run(runBlock);

    /** @ngInject */
    function runBlock($rootScope, $timeout, $state, authSettings, AuthService, gettextCatalog, msNavigationService,
                      NotifyService, fuseTheming, api)
    {
        var ln = localStorage.language||window.navigator.language||navigator.browserLanguage;
        $rootScope.languageDefault="es";
        gettextCatalog.currentLanguage = ln || $rootScope.languageDefault;
        $rootScope.languageSelected= ln || $rootScope.languageDefault;
        //por si viene con la sintaxis es-ES cogemos la primera parte solo
        $rootScope.languageSelected=$rootScope.languageSelected.split("-")[0];

        $rootScope.server = "";
        if(window.location.host.includes("localhost") || window.location.host.includes("192.168.2.")){
            $rootScope.server = "http://localhost:8000";
        }

        /*
         *
         *   LANGUAGES
         *
         */
        $rootScope.languages = [
            {
                code:'es',
                name:gettextCatalog.getString('Español')
            },
            {
                code:'en',
                name:gettextCatalog.getString('Inglés')
            },
            {
                code:'fr',
                name:gettextCatalog.getString('Francés')
            }
        ];

        $rootScope.changeLanguage=function(language){
            localStorage.language=language;
            window.location.reload();
        };


        /*
         *  Esta función nos permitirá llevar el control de permisos mediante URLs
         *
         * @param module
         * @param action
         */
        $rootScope.hasPermission=function(module,action){
            if(AuthService.currentUser && AuthService.currentUser.urlPermissions){
                var url=api.URLs[module];
                var method=action;
                if(action==="LIST" || action==="POST"){
                    url = url.replace(/:([^\/]*)[\/]$/g, "");
                    if(action==="LIST"){
                        method="GET";
                    }
                }
                url = url.replace(/:([^\/]*)[\/]/g, ":/");


                var urlPermission="/"+url+"["+method.toLowerCase()+"]"; //Ya tenemos formada la url para compararla con la de los permisos que nos da el backend

                return !!AuthService.currentUser.urlPermissions[urlPermission];
            }

            return true;
            // return false;
        };

        //Muestra mensaje de error
        $rootScope.showError=function(msg){
            NotifyService.errorMessage(msg);
        };


        // Activate loading indicator
        var stateChangeStartEvent = $rootScope.$on('$stateChangeStart', function ()
        {
            $rootScope.loadingProgress = true;
        });

        // De-activate loading indicator
        var stateChangeSuccessEvent = $rootScope.$on('$stateChangeSuccess', function ()
        {
            $timeout(function ()
            {
                $rootScope.loadingProgress = false;
            });
            $timeout(function ()
            {
                if(msNavigationService.getActiveItem()){
                    var node=msNavigationService.getActiveItem().node;
                    if(node.hidden()){
                        $rootScope.$broadcast(authSettings.ON_UNAUTHORIZED_REQUEST, AuthService.currentUser);
                    }
                }
            },500);
        });

        // Store state in the root scope for easy access
        $rootScope.state = $state;

        // Cleanup
        $rootScope.$on('$destroy', function ()
        {
            stateChangeStartEvent();
            stateChangeSuccessEvent();
        });

        // Si se detecta una petición no autorizada redirigir al login
        $rootScope.$on(authSettings.ON_UNAUTHORIZED_REQUEST, function (event, currentUser) {
            if (authSettings.LOGIN_STATE) {
                if(currentUser){
                    $state.go(authSettings.LOGIN_STATE_SUCCESS);
                }else{
                    $state.go(authSettings.LOGIN_STATE);
                }
            } else {
                console.warn("No ha definido una ruta para el formulario de login");
            }
        });

        // Si se detecta un logout, redirigir al login
        $rootScope.$on(authSettings.ON_LOGOUT_BROADCAST, function () {
            if (authSettings.LOGIN_STATE) {
                $state.go(authSettings.LOGIN_STATE);
                window.location.reload();
            } else {
                console.warn("No ha definido una ruta para el formulario de login");
            }
        });

        //creacion de eventos relacionados con las acciones login y logout
        $rootScope.$on(authSettings.ON_LOGIN_BROADCAST, function(event, currentUser){
            if (authSettings.LOGIN_STATE_SUCCESS) {
                if (currentUser.type_user === 'Manager'){
                    $state.go('app.programs');
                }else{
                    $state.go(authSettings.LOGIN_STATE_SUCCESS);
                }
            } else {
                console.warn("No ha definido una ruta para la redirección despues del login");
            }
        });

    }
})();
