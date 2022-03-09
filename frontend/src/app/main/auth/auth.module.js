(function () {
    'use strict';

    angular
        .module('app.auth', [])
        .config(config);

    /** @ngInject */
    function config($stateProvider, msApiProvider) {
        $stateProvider.state('app.auth', {
            abstract: true,
            url: '/auth'
        })

        // State
        .state('app.auth.login', {
            url: '/login',
            views: {
                'main@': {
                    templateUrl: 'app/core/layouts/content-only.html',
                    controller: 'MainController as vm'
                },
                'content@app.auth.login': {
                    templateUrl: 'app/main/auth/views/login/login.html',
                    controller: 'LoginController as vm'
                }
            },
            bodyClass: 'login'
        })
        // State
        .state('app.auth.register', {
            url      : '/register',
            views    : {
                'main@'                                 : {
                    templateUrl: 'app/core/layouts/content-only.html',
                    controller : 'MainController as vm'
                },
                'content@app.auth.register': {
                    templateUrl: 'app/main/auth/views/register/register.html',
                    controller : 'RegisterController as vm'
                }
            },
            bodyClass: 'register'
        });

        msApiProvider.setBaseUrl('api/');

        // Api
        msApiProvider.register('auth.login', ['auth/login/']);
        msApiProvider.register('auth.logout', ['auth/logout/']);
        msApiProvider.register('auth.currentUser', ['user/current_user/']);
        msApiProvider.register('auth.reset', ['authentication/reset_password/']);
        // msApiProvider.register('auth.resetConfirm', ['roles/reset_confirm_password/']);
        msApiProvider.register('auth.register', ['user']);
        // msApiProvider.register('auth.permissions', ['pydrfpermissions/pydrfpermissions/']);

    }

})();