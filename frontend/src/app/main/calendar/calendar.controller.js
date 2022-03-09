(function ()
{
    'use strict';

    angular
        .module('app.calendar')
        .controller('CalendarController', CalendarController);

    /** @ngInject */
    function CalendarController($scope, currentUser, Kpis, KpisPositive, usersService, $mdDialog, $document, eventsService,
                                DebounceService, $q, $state, cacheFactory)
    {
        var vm = this;

        // Data
        vm.user = currentUser;
        vm.kpis=Kpis;
        vm.kpisPositive=KpisPositive;

        vm.events = [];
        vm.leads=eventsService.leads;

        vm.selectedTabIndex=0;

        // Watchers
        $scope.$watch('vm.leads.filters', DebounceService(reloadCalendar, 300), true);
        $scope.$watch('vm.kpis.filters', DebounceService(eventsService.reloadKpis, 300), true);
        $scope.$watch('vm.kpisPositive.filters', DebounceService(eventsService.reloadKpisPositive, 300), true);

        vm.calendarUiConfig = {
            calendar: {
                defaultView       : 'month',
                locale            : 'es',
                lang              : 'es',
                editable          : false,
                eventLimit        : true,
                header            : '',
                handleWindowResize: false,
                aspectRatio       : 1,
                //hiddenDays        : [ 0 ],
                slotDuration      : '00:30:00',
                minTime           : "08:00:00",
                maxTime           : "22:00:00",
                slotLabelFormat   : "HH:mm",
                allDayText        : 'Todo el día',
                viewRender        : function (view)
                {
                    vm.calendarView = view;
                    vm.calendar = vm.calendarView.calendar;
                    vm.currentMonthShort = vm.calendar.getDate().format('MMMM');
                    vm.currentDate = vm.calendar.getDate().format('DD-MM-YYYY');
                },
                lazyFetching      : false,
                eventClick        : select,
                selectable        : false,
                selectHelper      : !!vm.user,
                eventRender       : eventRender,
                views: {
                    agendaDay: { // name of view
                        titleFormat: 'dddd, DD [de] MMMM [de] YYYY'
                    }
                },
                timeFormat: 'H:mm'
            }
        };

        // Methods
        vm.next = next;
        vm.prev = prev;
        vm.togglePositive = togglePositive;
        vm.toggleKpi = toggleKpi;
        vm.toggleKpiPositive = toggleKpiPositive;
        vm.getUsers = getUsers;
        vm.getFullUserName = getFullUserName;

        //////////
        reloadCalendar();
        function reloadCalendar(){
            var deferred = $q.defer();

            vm.events = eventsService.getEvents();
            $('#calendarView').fullCalendar('refetchEvents');

            deferred.resolve(vm.events);

            return deferred.promise;
        }

        /**
         * Go to next on current view (week, month etc.)
         */
        function select(event)
        {
            // $state.go('app.leads.get.edit',{lead: event.id});
            var url = $state.href('app.leads.get.edit', {lead: event.id});
            window.open(url,'_blank');
        }

        /**
         * Go to next on current view (week, month etc.)
         */
        function next()
        {
            vm.calendarView.calendar.next();
        }

        /**
         * Go to previous on current view (week, month etc.)
         */
        function prev()
        {
            vm.calendarView.calendar.prev();
        }

        function eventRender( event, element, view ) {
            var parent=$(element).find(".fc-content");
            setTimeout(function(){
                if(event.description){
                    var description=$("<span>("+event.description+")</span>");
                    parent.append(description);
                }

            },100);
        }



        /**
         * Activa/Desactiva el filtro de ganados
         *
         * @param active
         */
        function togglePositive() {
            for(var kpi in vm.kpis.data){
              for(var k in vm.kpis.data[kpi].kpis){
                vm.kpis.data[kpi].kpis[k].active=false;
              }
            }
            for(var kpi in vm.kpisPositive.data){
              for(var k in vm.kpisPositive.data[kpi].kpis){
                vm.kpisPositive.data[kpi].kpis[k].active=false;
              }
            }
            delete vm.leads.filters.kpi_filter;

            if(vm.selectedTabIndex===1 || vm.selectedTabIndex==='1'){
              vm.leads.filters.result='positive';
            }else{
              delete vm.leads.filters.result;
            }
        }

        /**
         * Activa/Desactiva el filtro del kpi
         *
         * @param item
         */
        function toggleKpi(item) {
            for(var kpi in vm.kpis.data){
                for(var k in vm.kpis.data[kpi].kpis){
                  vm.kpis.data[kpi].kpis[k].active=false;
                }
            }
            if(vm.leads.filters.kpi_filter===item.filter_key){
                item.active=false;
                vm.leads.filters.kpi_filter=null;
            }else{
                item.active=true;
                vm.leads.filters.kpi_filter=item.filter_key;
            }
        }

        /**
         * Activa/Desactiva el filtro del kpi
         *
         * @param item
         */
        function toggleKpiPositive(item) {
            for(var kpi in vm.kpisPositive.data){
                for(var k in vm.kpisPositive.data[kpi].kpis){
                  vm.kpisPositive.data[kpi].kpis[k].active=false;
                }
            }
            if(vm.leads.filters.kpi_filter===item.filter_key){
                item.active=false;
                vm.leads.filters.kpi_filter=null;
            }else{
                item.active=true;
                vm.leads.filters.kpi_filter=item.filter_key;
            }
        }

        /* Usuarios */
        function getUsers(searchText) {
            var deferred = $q.defer();
            var users = angular.copy(cacheFactory.usersService.get(searchText));
            if(!users){
                usersService.users.filters = {};
                usersService.users.filters.search = searchText;
                usersService.users.filters.page_size = "50";
                usersService.users.filters.is_complex = false;
                usersService.getUsers(searchText).then(function (users) {
                  cacheFactory.usersService.put(searchText, users);
                  deferred.resolve(users.data);
                });
            }else{
                deferred.resolve(users.data);
            }

            return deferred.promise;
        }

        function getFullUserName(user) {
            return user.first_name + " " + user.last_name;
        }

    }

})();
