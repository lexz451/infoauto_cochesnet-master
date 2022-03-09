
(function () {
    'use strict';

    angular
        .module('app.utils.factory', [])
        .factory('cacheFactory', cacheFactory);

    function cacheFactory($cacheFactory) {
        var cache = {
          usersService:$cacheFactory('usersService'),
          concessionairesService:$cacheFactory('concessionairesService'),
          originsService:$cacheFactory('originsService'),
          channelsService:$cacheFactory('channelsService'),
          vehiclesService:$cacheFactory('vehiclesService'),
          taskTypesService:$cacheFactory('taskTypesService'),
        };

        return  cache;
    }
})();
