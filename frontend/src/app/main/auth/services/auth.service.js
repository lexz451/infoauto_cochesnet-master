(function ()
{
    'use strict';

    angular
        .module('app.auth')
        .factory("AuthService", AuthService);


    /** @ngInject */
    function AuthService ( $q, $rootScope, authSettings, msApi, localStorageService, api) {
        var service = {
            loggedIn : false,
            token: '',
            currentUser : null,
            getCurrentUser : getCurrentUser,
            changeProfile : changeProfile,
            checkStatus: checkStatus,
            login: login,
            logout: logout,
            register: register,
            toggleOnline: toggleOnline,
            password: {
                resetRequest: passwordResetRequest,
                resetConfirm: passwordResetConfirm,
                change: passwordChange
            }
        };

        return service;

        /////////////

        /**
         * Comprueba el estado de identificación del usuario actual
         */
        function checkStatus ( )
        {
            var deferred = $q.defer();

            msApi.request('auth.currentUser@get', {}, function(res){
                if (res){
                    for(var i in res.profiles){
                        for(var j in res.profiles[i]){
                            if(res.profiles[i][j].id===localStorageService.get('token')){
                                res.profile=res.profiles[i][j];
                                res.type_user=res.profiles[i][j].profile_type;
                            }
                        }
                    }

                    service.loggedIn = true;
                    //res.is_admin=false;
                    //res.is_concession_admin=false;
                    service.currentUser = res;
                    service.token = localStorageService.get('token');

                    deferred.resolve(service.currentUser);
                    // msApi.request('auth.permissions@get', {}, function(res) {
                    //     service.currentUser.urlPermissions=res;
                    //     deferred.resolve(service.currentUser);
                    // });
                } else {
                    deferred.reject({error:"No hay ningún usuario autenticado"});
                }
            }, function(){
                deferred.reject({error:"No hay ningún usuario autenticado"});
            });

            return deferred.promise;
        }

        /**
         * Devuelve el usuario logueado
         */
        function getCurrentUser ( )
        {
            var deferred = $q.defer();

            if(service.currentUser){
                deferred.resolve(service.currentUser);
            }else{
                service.checkStatus().then(function(){
                    deferred.resolve(service.currentUser);
                },function(){
                    deferred.reject({error:"No hay ningún usuario autenticado"});
                });
            }

            return deferred.promise;
        }

        /**
         * Cambia de perfil
         */
        function changeProfile ( profile )
        {
            service.token = profile.id;
            localStorageService.set('token', service.token);

            service.currentUser.profile=profile;
            service.currentUser.type_user=profile.profile_type;

            if (authSettings.ON_LOGIN_BROADCAST) {
                $rootScope.$broadcast(authSettings.ON_LOGIN_BROADCAST, service.currentUser);
            }
            location.reload();
        }

        /**
         * Realiza la acción / intento de login
         */
        function login (username, password, noevent )
        {
            var deferred = $q.defer();
            localStorageService.remove('token');
            localStorageService.remove('tokenImpersonate');

            msApi.request('auth.login@save', {username: username, password: password}, function(res){
                // On login success
                service.loggedIn = true;
                service.token = res.token;
                localStorageService.set('token', service.token);

                //service.currentUser = res.user;
                service.checkStatus().then(function(data){
                    if ( authSettings.ON_LOGIN_BROADCAST && noevent !== true) {
                        $rootScope.$broadcast(authSettings.ON_LOGIN_BROADCAST, data);
                    }
                    deferred.resolve(res);
                }, function(){
                    // On detail fail
                    deferred.reject({error: "Error al obtener los datos del usuario"});
                });

            }, function(){
                // On login fail
                deferred.reject({error: "Nombre de usuario o contraseña incorrecta"});
            });

            return deferred.promise;
        }

        /**
         * Realiza la acción de logout
         */
        function logout ()
        {
            var deferred = $q.defer();
            msApi.request('auth.logout@save', function(res){
                service.loggedIn = false;
                service.currentUser = null;
                service.token = null;
                localStorageService.remove('token');
                localStorageService.remove('tokenImpersonate');



                if ( authSettings.ON_LOGOUT_BROADCAST) {
                    $rootScope.$broadcast(authSettings.ON_LOGOUT_BROADCAST);
                }
            }, function(res){
                // On logout fail
                deferred.reject(res);
            });

        }


        /**
         * Realiza la acción de solicitud de reseteo de contraseña
         */
        function passwordResetRequest ( form )
        {
            var deferred = $q.defer();

            msApi.request('auth.reset@save', form, function(res){
                if (res){
                    deferred.resolve(res);
                } else {
                    deferred.reject({error:"No hay ningún usuario con este email"});
                }
            }, function(error){
                deferred.reject(error);
            });

            return deferred.promise;
        }

        /**
         * Realiza la acción de confirmación de reseteo de contraseña
         */
        function passwordResetConfirm ( form )
        {
            var deferred = $q.defer();

            msApi.request('auth.resetConfirm@save', form, function(res){
                // On login success
                service.loggedIn = true;
                service.token = res.token;
                localStorageService.set('token', service.token);

                //service.currentUser = res.user;
                service.checkStatus().then(function(data){
                    if ( authSettings.ON_LOGIN_BROADCAST) {
                        $rootScope.$broadcast(authSettings.ON_LOGIN_BROADCAST, data);
                    }
                    deferred.resolve(res);
                });
            }, function(res){
                deferred.reject(res);
            });

            return deferred.promise;
        }

        /**
         * Realiza la acción de cambio de contraseña
         */
        function passwordChange ( oldPassword, newPassword, newPasswordRepeat )
        {
            var deferred = $q.defer();

            api.user.passwordChange({current_password: oldPassword, password: newPassword, password_repeat: newPasswordRepeat}, function(){
                deferred.resolve();
            }, function(res){
                // On password fail
                deferred.reject(res.data);
            });

            return deferred.promise;
        }

        /**
         * Realiza el registro de una empresa
         */
        function register ( form )
        {
            var deferred = $q.defer();

            localStorageService.remove('token');
            localStorageService.remove('tokenImpersonate');
            msApi.request('auth.register@save', form, function(res){

                service.loggedIn = true;
                service.token = res.token;
                localStorageService.set('token', service.token);

                //service.currentUser = res.user;
                service.checkStatus().then(function(data){
                    if ( authSettings.ON_LOGIN_BROADCAST) {
                        $rootScope.$broadcast(authSettings.ON_LOGIN_BROADCAST, data);
                    }
                    deferred.resolve(res);
                });

            }, function(error){
                deferred.reject(error);
            });

            return deferred.promise;
        }

        /**
         * Cambia el estado de la sesión
         */
        function toggleOnline ()
        {
            var deferred = $q.defer();

            api.users.sessionStatus({}, updateOK, saveKO);

            return deferred.promise;

            function updateOK(response) {
                service.currentUser.session.online=response.forced_online_status;
                deferred.resolve(response);
            }

            function saveKO(response) {
                deferred.reject(response);
            }

        }

    }

})();
