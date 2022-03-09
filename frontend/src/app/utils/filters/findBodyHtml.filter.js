(function () {
    'use strict';

    angular
        .module('app.utils.filters')
        .filter('findBodyHtml', findBodyHtml);

    function findBodyHtml() {
        return function(html){
            var strVal = html; //obviously, this line can be omitted - just assign your string to the name strVal or put your string var in the pattern.exec call below
            var pattern = /<body[^>]*>((.|[\n\r])*)<\/body>/im;
            var array_matches = pattern.exec(strVal);

            return array_matches || html;
        };
    }
})();
