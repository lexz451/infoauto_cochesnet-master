(function () {
    'use strict';

    angular
        .module('app.utils.filters', []
        )
        .config(config)
        .filter('formatTime', formatTime);

    /** @ngInject */
    function config() {


    }

    function formatTime($filter) {
        return function (time, format) {
            var parts = time.split(':');
            var date = new Date(0, 0, 0, parts[0], parts[1], parts[2]);
            return $filter('date')(date, format || 'HH:mm');
        };

    }
})();
