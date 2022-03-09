
(function () {
    'use strict';

    angular
        .module('app.utils.filters')
        .filter('durationHumanize', durationHumanize);

    function durationHumanize(moment) {
        return function(input) {
            return moment.duration(input, "minutes").format("D [días], h [horas], m [minutos]");
        }
    }
})();
