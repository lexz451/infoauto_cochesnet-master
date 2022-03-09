(function (window, angular, undefined) {
    'use strict';

    angular
        .module('app.utils.directives')
        .directive('iframeAuthentication', iframeAuthentication);

    /** @ngInject */
    function iframeAuthentication($http, $rootScope) {
        return {
            restrict: 'E',
            scope: {
                src: '='
            },
            link: function (scope, element) {
                $http({
                    method: 'GET',
                    url: scope.src
                }).then(function successCallback(response) {
                    getOK(response);
                });

                function getOK(response){
                    var iframe = $(element);
                    var str=response.data;

                    var p1=str.indexOf("<body");
                    var p2=str.indexOf("</body>")+7;

                    str = str.slice(p1, p2);

                    str=str.replace("<body","<div");
                    str=str.replace("</body>","</div>");

                    if($rootScope.server){
                        str = str.replace(/<img[^<]*src=["']([^"]*)["']/g, "<img src='"+$rootScope.server+"$1'");
                    }

                    iframe.html(str);
                }
            }
        };
    }

})(window, angular);
