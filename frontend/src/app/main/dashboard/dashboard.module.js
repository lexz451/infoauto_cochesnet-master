(function () {
    'use strict';

    angular
        .module('app.dashboard',
            [

            ]
        )
        .config(config);

    /** @ngInject */
    function config($stateProvider) {

        // State
        $stateProvider.state('app.dashboard', {
            url      : '/dashboard',
            views    : {
                'content@app': {
                    templateUrl: 'app/main/dashboard/dashboard.html',
                    controller : 'DashboardController as vm'
                }
            },
            resolve  : {
                currentUser: function (AuthService)
                {
                    return AuthService.getCurrentUser().then(function (response) {
                        if (response) {
                            return response;
                        }
                    });
                },
                Dashboards: function (currentUser, dashboardService) {
                    dashboardService.dashboards.filters={};
                    dashboardService.dashboards.filters.page_size="all";
                    return dashboardService.getDashboards();
                }
            },
            bodyClass: 'todo'
        });


    }
})();
