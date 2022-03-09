(function () {
    'use strict';

    angular
        .module('app.toolbar')
        .controller('ToolbarController', ToolbarController);

    /** @ngInject */
    function ToolbarController($rootScope, $q, $state, $timeout, $mdSidenav, $mdToast, msNavigationService, usersService, $mdDialog, $document,
                               $scope, authSettings, localStorageService, AuthService, leadsService, scoresService, leadStatusService) {
        var vm = this;

        // Data
        vm.authService=AuthService;
        vm.user=AuthService.currentUser;
        AuthService.getCurrentUser().then(function (response) {
            if (response) {
                // getReadPending();
            }
        });

        vm.bodyEl = angular.element('body');

        vm.scores=scoresService.scores;
        vm.lead=leadsService.lead;
        vm.leadStatus=leadStatusService.leadStatus;

        // Watchers
        $scope.$watch('vm.authService', function(){
            vm.user=AuthService.currentUser;
        }, true);

        // Methods
        vm.toggleSidenav = toggleSidenav;
        vm.logout = logout;
        vm.toggleHorizontalMobileMenu = toggleHorizontalMobileMenu;
        vm.toggleMsNavigationFolded = toggleMsNavigationFolded;
        vm.showInfo = showInfo;
        vm.toggleOnline = toggleOnline;
        vm.getFullNameUser = getFullNameUser;
        vm.toggleAvailable = toggleAvailable;

        //////////

        /**
         * Toggle sidenav
         *
         * @param sidenavId
         */
        function toggleSidenav(sidenavId) {
            $mdSidenav(sidenavId).toggle();
        }

        /**
         * Devuelve si se debe mostrar el desplegable de informacion de lead
         */
        function showInfo() {
            return ($state.current.name==='app.leads.get.edit');
        }

        /**
         * Logout Function
         */
        function logout() {
            // Do logout here.
            AuthService.logout();
        }

        /**
         * Toggle horizontal mobile menu
         */
        function toggleHorizontalMobileMenu() {
            vm.bodyEl.toggleClass('ms-navigation-horizontal-mobile-menu-active');
        }

        /**
         * Toggle msNavigation folded
         */
        function toggleMsNavigationFolded() {
            msNavigationService.toggleFolded();
        }

        /**
         * Marca como activo o inactivo a un usuario
         */
        function toggleOnline(){
            AuthService.toggleOnline();
        }

        function getFullNameUser(user){
            var text=(user.first_name || '')+" "+(user.last_name || '');
            if(text===" "){
                text=user.email;
            }
            return text;
        }

        /**
         * Marca como disponible o no disponible a un usuario
         */
        function toggleAvailable(sw){
            if(!sw){
                openAvailableDialog(vm.user)
            }else{
                var obj={
                    id:vm.user.id,
                    is_available:sw,
                    unavailable_reason:''
                };
                return usersService.saveUser(obj).then(function(res){
                    vm.user.is_available=res.is_available;
                })
            }
        }

        /**
         * Abre el dialogo para crear/editar una user
         *
         * @param ev
         * @param user
         */
        function openAvailableDialog(user) {
            $mdDialog.show({
                controller: 'AvailableDialogController',
                controllerAs: 'vm',
                templateUrl: 'app/main/users/dialogs/available/available-dialog.html',
                parent: angular.element($document.body),
                clickOutsideToClose: true,
                locals: {
                    User:user
                }
            }).then(function(res) {
                vm.user.is_available=res.is_available;
            });
        }
    }

})();
