(function () {
    'use strict';

    angular
        .module('app.utils.directives')
        .directive('uniqueEmail', uniqueEmail);

    /** @ngInject */
    function uniqueEmail(api, $q) {
        return {
            require: 'ngModel',
            link: function (scope, element, attrs, ctrl) {
                ctrl.$asyncValidators.unique = function (modelValue, viewValue) {
                    var deferred = $q.defer();

                    api.user.emailCheck({email: viewValue}, function(data){
                        if (data.exists){
                            deferred.reject();
                        } else {
                            deferred.resolve();
                        }
                    });

                    return deferred.promise;
                };
            }
        };
    }
})();
