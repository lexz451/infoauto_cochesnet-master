(function () {
    'use strict';

    angular
        .module('app.users')
        .controller('UserController', UserController);

    /** @ngInject */
    function UserController(currentUser, User, professionalProfilesService) {
        var vm = this;

        // Data
        vm.user=User;

        vm.professional_profiles=professionalProfilesService.professionalProfiles;


    }
})();
