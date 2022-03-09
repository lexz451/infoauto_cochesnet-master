(function () {
    'use strict';

    angular
        .module('app.leads',
            [

            ]
        )
        .config(config);

    /** @ngInject */
    function config($stateProvider) {

        $stateProvider
            .state('app.leads', {
                abstract: true,
                url: '/leads',
                resolve:{
                    currentUser: function (AuthService){
                        return AuthService.getCurrentUser().then(function (response) {
                            if (response) {
                                return response;
                            }
                        });
                    }
                }
            })
            .state('app.leads.list', {
                url: '/?created_start_date&created_end_date&user_id__in&tasks__realization_date_check&tasks__is_traking_task&' +
                  'with_concession&without_pending_tasks&tasks__planified_realization_date__lt&tasks__realization_date__isnull&' +
                  'without_pending_trackings&result&source__channel_id__in&tasks__media__in&result__isnull&lead_managements__event&' +
                  'without_outgoing_calls',
                views: {
                    'content@app': {
                        templateUrl: 'app/main/leads/views/list/leads.html',
                        controller: 'LeadsController as vm'
                    }
                },
                resolve: {
                    Leads: function (currentUser, $rootScope, leadsService, $stateParams) {
                        leadsService.leads.filters=$stateParams;
                        if(!$stateParams.created_start_date){
                          leadsService.leads.filters.user_id__in=currentUser.id;
                        }
                        return leadsService.getLeads();
                    },
                    Kpis: function (currentUser, $rootScope, eventsService) {
                        eventsService.kpis.filters={};
                        return eventsService.getKpis();
                    }
                },
                bodyClass: 'leads'
            })
            .state('app.leads.board', {
                url: '/board',
                views: {
                    'content@app': {
                        templateUrl: 'app/main/leads/views/board/board-view.html',
                        controller: 'BoardViewController as vm'
                    }
                },
                resolve: {
                    Today: function(){
                        var d=new Date();
                        d.setHours(0,0,0,0);
                        return d;
                    },
                    PageSize: function(){
                        return 10;
                    },
                    LeadsNews: function (currentUser, leadsService, Today, PageSize) {
                        leadsService.leadsNews.filters={};
                        leadsService.leadsNews.filters.page_size=PageSize;
                        leadsService.leadsNews.filters.page=1;
                        leadsService.leadsNews.filters.ordering='created';
                        leadsService.leadsNews.filters.with_concession=true;
                        return leadsService.getLeadsNews();
                    },
                    LeadsAttended: function (currentUser, leadsService, Today, PageSize) {
                        leadsService.leadsAttended.filters={};
                        leadsService.leadsAttended.filters.page_size=PageSize;
                        leadsService.leadsAttended.filters.page=1;;
                        leadsService.leadsAttended.filters.ordering='created';
                        leadsService.leadsAttended.filters.with_concession=true;
                        return leadsService.getLeadsAttended();
                    },
                    LeadsCommercialManagements: function (currentUser, leadsService, Today, PageSize) {
                        leadsService.leadsCommercialManagements.filters={};
                        leadsService.leadsCommercialManagements.filters.page_size=PageSize;
                        leadsService.leadsCommercialManagements.filters.page=1;
                        leadsService.leadsCommercialManagements.filters.ordering='lead_task_date';
                        leadsService.leadsCommercialManagements.filters.with_concession=true;
                        return leadsService.getLeadsCommercialManagements();
                    },
                    LeadsTracings: function (currentUser, leadsService, Today, PageSize) {
                        leadsService.leadsTracings.filters={};
                        leadsService.leadsTracings.filters.page_size=PageSize;
                        leadsService.leadsTracings.filters.page=1;
                        leadsService.leadsTracings.filters.ordering='lead_task_date';
                        leadsService.leadsTracings.filters.with_concession=true;
                        return leadsService.getLeadsTracings();
                    },
                    LeadsEnds: function (currentUser, leadsService, Today, PageSize) {
                        leadsService.leadsEnds.filters={};
                        leadsService.leadsEnds.filters.page_size=PageSize;
                        leadsService.leadsEnds.filters.page=1;
                        leadsService.leadsEnds.filters.with_concession=true;
                        return leadsService.getLeadsEnds();
                    },
                    Actions: function(currentUser, leadActionsService){
                        return leadActionsService.getLeadActionsColumn();
                    }
                },
                bodyClass: 'leads'
            })
            .state('app.leads.allboard', {
                url: '/all',
                views: {
                    'content@app': {
                        templateUrl: 'app/main/leads/views/board/board-view.html',
                        controller: 'BoardViewController as vm'
                    }
                },
                resolve: {
                    PageSize: function(){
                        return 10;
                    },
                    LeadsNews: function (currentUser, leadsService, PageSize) {
                        leadsService.leadsNews.filters={};
                        leadsService.leadsNews.filters.page_size=PageSize;
                        leadsService.leadsNews.filters.with_concession=true;
                        return leadsService.getLeadsNews();
                    },
                    LeadsAttended: function (currentUser, leadsService, PageSize) {
                        leadsService.leadsAttended.filters={};
                        leadsService.leadsAttended.filters.page_size=PageSize;
                        leadsService.leadsAttended.filters.with_concession=true;
                        return leadsService.getLeadsAttended();
                    },
                    LeadsCommercialManagements: function (currentUser, leadsService, PageSize) {
                        leadsService.leadsCommercialManagements.filters={};
                        leadsService.leadsCommercialManagements.filters.page_size=PageSize;
                        leadsService.leadsCommercialManagements.filters.with_concession=true;
                        return leadsService.getLeadsCommercialManagements();
                    },
                    LeadsTracings: function (currentUser, leadsService, PageSize) {
                        leadsService.leadsTracings.filters={};
                        leadsService.leadsTracings.filters.page_size=PageSize;
                        leadsService.leadsTracings.filters.with_concession=true;
                        return leadsService.getLeadsTracings();
                    },
                    LeadsEnds: function (currentUser, leadsService, PageSize) {
                        leadsService.leadsEnds.filters={};
                        leadsService.leadsEnds.filters.page_size=PageSize;
                        leadsService.leadsEnds.filters.with_concession=true;
                        return leadsService.getLeadsEnds();
                    },
                    Actions: function(){
                        return false;
                    }
                },
                bodyClass: 'leads'
            })
            .state('app.leads.get', {
                abstract: true,
                url: '/:lead/',
                resolve:{
                    Lead: function (leadsService,$stateParams) {
                        if($stateParams.lead>0){
                            return leadsService.getLead($stateParams.lead);
                        }
                        leadsService.lead.data = {};
                        return leadsService.getEmptyLead();
                    },
                    Tasks: function (Lead, tasksService) {
                        tasksService.tasks.data=Lead.request.task;
                        tasksService.tasks.count=Lead.request.task.length;
                        return tasksService.tasks;
                    },
                    GasTypes: function (gasTypesService) {
                        return gasTypesService.getGasTypes();
                    },
                    Concessionaire: function (Lead, concessionairesService, $stateParams) {
                        if($stateParams.lead>0){
                            return Lead.concessionaire_data;
                        }
                        return {};
                    },
                    PageSize: function(){
                      return 10;
                    },
                    LeadsNews: function (currentUser, leadsService, PageSize, Lead) {
                      leadsService.leadsNews.filters={};
                      if(Lead.client){
                        leadsService.leadsNews.filters.client__phone__icontains=Lead.client.phone;
                        leadsService.leadsNews.filters.client__email__icontains=Lead.client.email;
                      }
                      leadsService.leadsNews.filters.id_excluded=Lead.id || 0;
                      leadsService.leadsNews.filters.page_size=PageSize;
                      leadsService.leadsNews.filters.ordering='created';
                      leadsService.leadsNews.filters.with_concession=true;
                      return leadsService.getLeadsNews();
                    },
                    LeadsAttended: function (currentUser, leadsService, PageSize, Lead) {
                      leadsService.leadsAttended.filters={};
                      if(Lead.client) {
                        leadsService.leadsAttended.filters.client__phone__icontains = Lead.client.phone;
                        leadsService.leadsAttended.filters.client__email__icontains = Lead.client.email;
                      }
                      leadsService.leadsAttended.filters.id_excluded=Lead.id || 0;
                      leadsService.leadsAttended.filters.page_size=PageSize;
                      leadsService.leadsAttended.filters.ordering='created';
                      leadsService.leadsAttended.filters.with_concession=true;
                      return leadsService.getLeadsAttended();
                    },
                    LeadsCommercialManagements: function (currentUser, leadsService, PageSize, Lead) {
                      leadsService.leadsCommercialManagements.filters={};
                      if(Lead.client) {
                        leadsService.leadsCommercialManagements.filters.client__phone__icontains = Lead.client.phone;
                        leadsService.leadsCommercialManagements.filters.client__email__icontains = Lead.client.email;
                      }
                      leadsService.leadsCommercialManagements.filters.id_excluded=Lead.id || 0;
                      leadsService.leadsCommercialManagements.filters.page_size=PageSize;
                      leadsService.leadsCommercialManagements.filters.ordering='lead_task_date';
                      leadsService.leadsCommercialManagements.filters.with_concession=true;
                      return leadsService.getLeadsCommercialManagements();
                    },
                    LeadsTracings: function (currentUser, leadsService, PageSize, Lead) {
                      leadsService.leadsTracings.filters={};
                      if(Lead.client) {
                        leadsService.leadsTracings.filters.client__phone__icontains = Lead.client.phone;
                        leadsService.leadsTracings.filters.client__email__icontains = Lead.client.email;
                      }
                      leadsService.leadsTracings.filters.id_excluded=Lead.id || 0;
                      leadsService.leadsTracings.filters.page_size=PageSize;
                      leadsService.leadsTracings.filters.ordering='lead_task_date';
                      leadsService.leadsTracings.filters.with_concession=true;
                      return leadsService.getLeadsTracings();
                    },
                    LeadsEnds: function (currentUser, leadsService, PageSize, Lead) {
                      leadsService.leadsEnds.filters={};
                      if(Lead.client) {
                        leadsService.leadsEnds.filters.client__phone__icontains = Lead.client.phone;
                        leadsService.leadsEnds.filters.client__email__icontains = Lead.client.email;
                      }
                      leadsService.leadsEnds.filters.id_excluded=Lead.id || 0;
                      leadsService.leadsEnds.filters.page_size=PageSize;
                      leadsService.leadsEnds.filters.with_concession=true;
                      return leadsService.getLeadsEnds();
                    },
                }
            })
            .state('app.leads.get.detail', {
                url      : 'detail',
                views    : {
                    'content@app': {
                        templateUrl: 'app/main/leads/views/detail/lead.html',
                        controller : 'LeadController as vm'
                    }
                },
                bodyClass: 'todo'
            })
            .state('app.leads.get.edit', {
                //Estos parámetros get son para el ACD
                url      : 'edit?source&phone&acd&user',
                views    : {
                    'content@app': {
                        templateUrl: 'app/main/leads/views/edit/lead.html',
                        controller : 'LeadEditController as vm'
                    }
                },
                resolve:{
                    Concessionaire: function (Lead, concessionairesService, $stateParams) {
                        if($stateParams.lead>0){
                            return Lead.concessionaire_data;
                        }
                        return {};
                    },
                    Source: function (sourcesService, $stateParams) {
                        if($stateParams.source){
                            return sourcesService.getSource($stateParams.source);
                        }
                        return {};
                    },
                    LeadsIncomingCalls: function (leadsService, $stateParams) {
                        if($stateParams.lead>0){
                            return leadsService.getLeadsIncomingCalls($stateParams.lead);
                        }
                        return {};
                    },
                    LeadsOutgoingCalls: function (leadsService, $stateParams) {
                        if($stateParams.lead>0){
                            return leadsService.getLeadsOutgoingCalls($stateParams.lead);
                        }
                        return {};
                    },
                    LeadsHistory: function (leadsService, $stateParams) {
                        if($stateParams.lead>0){
                            return leadsService.getLeadsHistory($stateParams.lead);
                        }
                        return {};
                    },
                    LeadsActivity: function (leadsService, $stateParams) {
                        if($stateParams.lead>0){
                            return leadsService.getLeadsActivity($stateParams.lead);
                        }
                        return {};
                    },
                    StartCall: function () {
                        return false;
                    }
                },
                bodyClass: 'todo'
            })
            .state('app.leads.get.call', {
                //Estos parámetros get son para el ACD
                url      : 'call',
                views    : {
                    'content@app': {
                        templateUrl: 'app/main/leads/views/edit/lead.html',
                        controller : 'LeadEditController as vm'
                    }
                },
                resolve:{
                    Concessionaire: function (Lead, concessionairesService, $stateParams) {
                        if($stateParams.lead>0){
                            return Lead.concessionaire_data;
                        }
                        return {};
                    },
                    Source: function (sourcesService, $stateParams) {
                        if($stateParams.source){
                            return sourcesService.getSource($stateParams.source);
                        }
                        return {};
                    },
                    LeadsIncomingCalls: function (leadsService, $stateParams) {
                        if($stateParams.lead>0){
                            return leadsService.getLeadsIncomingCalls($stateParams.lead);
                        }
                        return {};
                    },
                    LeadsOutgoingCalls: function (leadsService, $stateParams) {
                        if($stateParams.lead>0){
                            return leadsService.getLeadsOutgoingCalls($stateParams.lead);
                        }
                        return {};
                    },
                    LeadsHistory: function (leadsService, $stateParams) {
                        if($stateParams.lead>0){
                            return leadsService.getLeadsHistory($stateParams.lead);
                        }
                        return {};
                    },
                    LeadsActivity: function (leadsService, $stateParams) {
                        if($stateParams.lead>0){
                            return leadsService.getLeadsActivity($stateParams.lead);
                        }
                        return {};
                    },
                    StartCall: function () {
                        return true;
                    }
                },
                bodyClass: 'todo'
            });

    }
})();
