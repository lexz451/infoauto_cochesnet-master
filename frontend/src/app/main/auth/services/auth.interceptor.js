(function () {
    'use strict';

    angular
        .module('app.auth')
        .config(interceptor);

    function interceptor($provide, $httpProvider, authSettings, AuthServiceProvider) {

        // Este interceptor captura todos los fallos de autenticación
        $provide.factory('AuthenticationInterceptor', ['localStorageService', '$q', '$rootScope', function (localStorageService, $q, $rootScope) {
            return {
                request: function(config) {
                    config.headers = config.headers || {};
                    if (localStorageService.get('token')) {
                        config.headers.Authorization = 'Token ' + localStorageService.get('token');
                    }
                    if (localStorageService.get('tokenImpersonate')) {
                        config.headers.ImpersonateAuthorization = 'Token ' + localStorageService.get('tokenImpersonate');
                    }
                    if($rootScope.languageSelected){
                       config.headers['Accept-Language'] = $rootScope.languageSelected;
                    }
                    return config || $q.when(config);
                },

                // Utilizamos el método response error ya que queremos capturar los 401
                responseError: function (rejection) {
                    if (rejection.status === 401 || rejection.status === 403) {

                        if (authSettings.ON_UNAUTHORIZED_REQUEST && localStorageService.get('token')){
                            AuthServiceProvider.$get().getCurrentUser().then(function(currentUser){
                                $rootScope.$broadcast(authSettings.ON_UNAUTHORIZED_REQUEST, currentUser);
                            });
                        }else{
                            $rootScope.$broadcast(authSettings.ON_UNAUTHORIZED_REQUEST);
                        }
                        localStorageService.remove('token');
                        localStorageService.remove('tokenImpersonate');

                    }

                    // Flujo normal de ejecución
                    return $q.reject(rejection);
                }
            };
        }]);

        // Add the interceptor to the $httpProvider.
        $httpProvider.interceptors.push('AuthenticationInterceptor');
    }
})();
