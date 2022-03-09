(function ()
{
    'use strict';

    angular
        .module('app.calendar',
            [
                // 3rd Party Dependencies
                'ui.calendar'
            ]
        )
        .config(config);

    /** @ngInject */
    function config($stateProvider)
    {
        // State
        $stateProvider
            .state('app.calendar', {
                url      : '/calendar',
                views    : {
                    'content@app': {
                        templateUrl: 'app/main/calendar/calendar.html',
                        controller : 'CalendarController as vm'
                    }
                },
                    resolve  : {
                        currentUser: function (AuthService){
                            return AuthService.getCurrentUser().then(function (response) {
                                if (response) {
                                    return response;
                                }
                            });
                        },
                        Kpis: function (currentUser, $rootScope, eventsService) {
                            eventsService.leads.filters={}
                            eventsService.leads.filters.user_data=currentUser;
                            eventsService.kpis.filters={};
                            return eventsService.kpis;
                        },
                        KpisPositive: function (currentUser, $rootScope, eventsService) {
                            eventsService.kpisPositive.filters={};
                            eventsService.kpisPositive.filters.result='positive';
                            return eventsService.kpisPositive;
                        }
                    },
                bodyClass: 'calendar'
            });

    }
})();
