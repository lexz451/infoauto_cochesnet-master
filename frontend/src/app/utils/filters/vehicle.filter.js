
(function () {
    'use strict';

    angular
        .module('app.utils.filters')
        .filter('vehicle', vehicle);

    function vehicle() {
        return function(text) {
            if(text){
                var arr=text.split(" ");
                var t='';
                for(var i=0; i<arr.length;i++){
                    t+=arr[i].split("___")[0]+" ";
                }
                return t;
            }
            return text;
        }
    }
})();
