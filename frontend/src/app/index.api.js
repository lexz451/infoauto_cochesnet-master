(function () {
    'use strict';

    angular
        .module('fuse')
        .factory('api', apiService);

    /** @ngInject */
    function apiService($resource) {
        var api = {};
        var queryAll = {
            method: 'GET',
            params: {
                page: 'all'
            },
            isArray: true
        };

        var queryAllObj = {
            method: 'GET',
            params: {
                page: 'all'
            }
        };

        var defaultObj={
            queryAll: queryAll,
            queryAllObj: queryAllObj,
            create: {method: 'POST'},
            update: {method: 'PATCH'},
        };

        // Base Url
        api.baseUrl = 'api/';

        api.URLs={};

        api.URLs.users=api.baseUrl + 'user/:id/';
        api.URLs.usersComplexCreate=api.baseUrl + 'user/complex_create/';
        api.URLs.usersComplexUpdate=api.baseUrl + 'user/:id/complex_update/';
        api.URLs.sessionStatus=api.baseUrl + 'session_historic/change_forced_online_status/';
        api.URLs.removeConcessionaire=api.baseUrl + 'user_concession/:id/';
        api.URLs.removeSFA=api.baseUrl + 'sfa/:id/';
        api.URLs.admins=api.baseUrl + 'user/:concessionaire/concession_manager_or_admin/';
        api.URLs.leads=api.baseUrl + 'lead/:id/';
        api.URLs.leadsReactivate=api.baseUrl + 'lead/:id/reactivate/';
        api.URLs.leadsMail=api.baseUrl + 'lead/:id/email/';
        api.URLs.leadsStatus=api.baseUrl + 'lead/:id/change_status/';
        api.URLs.kpis=api.baseUrl + 'lead_calendar/kpis/';
        api.URLs.leadActions=api.baseUrl + 'lead_actions/';
        api.URLs.leadActionsColumn=api.baseUrl + 'lead_actions/get_column/';
        api.URLs.leadsByUser=api.baseUrl + 'user/:id/list_user_leads/';
        api.URLs.setLeadsByUser=api.baseUrl + 'user/:id/set_user_leads/';
        api.URLs.vehicles=api.baseUrl + 'vehicles/:id/';
        api.URLs.appraisals=api.baseUrl + 'appraisal/:id/';

        // Campaigns
        api.URLs.campaigns=api.baseUrl + 'campaigns/';
        api.URLs.campaignsDetail=api.baseUrl + 'campaigns/:id/';


        api.URLs.leadsNews=api.baseUrl + 'lead_col/?status=new';
        api.URLs.leadsAttended=api.baseUrl + 'lead_col/?status=attended';
        api.URLs.leadsCommercialManagements=api.baseUrl + 'lead_col/?status=commercial_management';
        api.URLs.leadsTracings=api.baseUrl + 'lead_col/?status=tracing';
        api.URLs.leadsEnds=api.baseUrl + 'lead_col/?status=end';

        api.URLs.leadsHistory=api.baseUrl + 'lead_history/:id/get_history/';
        api.URLs.leadsIncomingCalls=api.baseUrl + 'lead-historic/:id/incoming_calls/';
        api.URLs.leadsOutgoingCalls=api.baseUrl + 'lead-historic/:id/outgoing_calls/';

        api.URLs.leadsClone=api.baseUrl + 'lead/:id/clone/';
        api.URLs.tasks=api.baseUrl + 'task/:id/';
        api.URLs.taskTypes=api.baseUrl + 'task/options/:id/';
        api.URLs.concessionaires=api.baseUrl + 'concessionaire/:id/';
        api.URLs.concessionairesConfig=api.baseUrl + 'concessionaire/config/';
        api.URLs.removeSource=api.baseUrl + 'source/:id/';
        api.URLs.gasTypes=api.baseUrl + 'gas_type/:id/';
        api.URLs.provinces=api.baseUrl + 'provinces/:id/';
        api.URLs.localities=api.baseUrl + 'localities/:id/';
        api.URLs.countries=api.baseUrl + 'countries/:id/';

        api.URLs.brands=api.baseUrl + 'vehicles_brand/:id/';
        api.URLs.models=api.baseUrl + 'vehicles_model/:id/';
        api.URLs.versions=api.baseUrl + 'vehicles_version/:id/';

        api.URLs.clients=api.baseUrl + 'clients/:id/';
        api.URLs.businessActivity=api.baseUrl + 'business_activity/:id/';
        api.URLs.sectors=api.baseUrl + 'business_sector/:id/';
        api.URLs.whatsapp=api.baseUrl + 'lead_whatsapp_message/:id/';

        api.URLs.origins=api.baseUrl + 'origin/:id/';
        api.URLs.channels=api.baseUrl + 'channel/:id/';
        api.URLs.sources=api.baseUrl + 'source/:id/';
        api.URLs.acds=api.baseUrl + 'netelip/call_manager/:id/';
        api.URLs.netelip=api.baseUrl + 'netelip/call_control_lead/:id/';
        api.URLs.phones=api.baseUrl + 'phone/:id/';
        api.URLs.emails=api.baseUrl + 'email/:id/';
        api.URLs.calendar=api.baseUrl + 'lead_calendar/';

        api.URLs.dashboards=api.baseUrl + 'concession-dashboard/:id/';
        api.URLs.benchmark=api.baseUrl + 'lead/dashboard_benchmark/:id/';
        api.URLs.servicelevel=api.baseUrl + 'lead/dashboard_service_level/:id/';
        api.URLs.voiceService=api.baseUrl + 'lead/dashboard_voice_service_level/:id/';
        api.URLs.digitalService=api.baseUrl + 'lead/dashboard_digital_service_level/:id/';

        api.URLs.click2calls=api.baseUrl + 'netelip/call_control_lead/click2call/:id/';
        api.URLs.leadsHubspot=api.baseUrl + 'lead/:id/update_hubspot/';

        var ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
        api.socket = ws_scheme +'://' + window.location.host + '/websocket/';
        if(window.location.host.includes("localhost") || window.location.host.includes("192.168.2.")){
            api.socket=ws_scheme +'://localhost:8000/ws/';
        }
        api.wsAcds=api.socket+'netelip/';

        // $resources
        api.users = $resource(api.URLs.users, {id: '@id'}, {
            queryAll: queryAll,
            queryAllObj: queryAllObj,
            create: {
                url:api.URLs.usersComplexCreate,
                method: 'POST'
            },
            update: {
                url:api.URLs.usersComplexUpdate,
                method: 'PATCH'
            },
            removeConcessionaire: {
                url:api.URLs.removeConcessionaire,
                method: 'DELETE'
            },
            removeSFA: {
                url:api.URLs.removeSFA,
                method: 'DELETE'
            },
            sessionStatus: {
                url:api.URLs.sessionStatus,
                method: 'PATCH'
            }
        });

        api.admins = $resource(api.URLs.admins, {concessionaire: '@concessionaire'}, defaultObj);

        api.leads = $resource(api.URLs.leads, {id: '@id'}, {
            queryAll: queryAll,
            queryAllObj: queryAllObj,
            create: {method: 'POST'},
            update: {method: 'PATCH'},
            clone: {
                url:api.URLs.leadsClone,
                method: 'POST'
            },
            leadsStatus: {
                url:api.URLs.leadsStatus,
                method: 'PATCH'
            },
            leadsHubspot: {
                url:api.URLs.leadsHubspot,
                method: 'POST'
            },
            kpis: {
                url:api.URLs.kpis,
                method: 'GET'
            }
        });

        api.leadActions = $resource(api.URLs.leadActions, {id: '@id'}, defaultObj);
        api.leadActionsColumn = $resource(api.URLs.leadActionsColumn, {id: '@id'}, defaultObj);
        api.leadsNews = $resource(api.URLs.leadsNews, {id: '@id'}, defaultObj);
        api.leadsReactivate = $resource(api.URLs.leadsReactivate, {id: '@id'}, defaultObj);
        api.leadsMail = $resource(api.URLs.leadsMail, {id: '@id'}, defaultObj);
        api.leadsAttended = $resource(api.URLs.leadsAttended, {id: '@id'}, defaultObj);
        api.leadsCommercialManagements = $resource(api.URLs.leadsCommercialManagements, {id: '@id'}, defaultObj);
        api.leadsTracings = $resource(api.URLs.leadsTracings, {id: '@id'}, defaultObj);
        api.leadsEnds = $resource(api.URLs.leadsEnds, {id: '@id'}, defaultObj);

        api.leadsHistory = $resource(api.URLs.leadsHistory, {id: '@id'}, defaultObj);
        api.leadsIncomingCalls = $resource(api.URLs.leadsIncomingCalls, {id: '@id'}, defaultObj);
        api.leadsOutgoingCalls = $resource(api.URLs.leadsOutgoingCalls, {id: '@id'}, defaultObj);

        api.leadsByUser = $resource(api.URLs.leadsByUser, {id: '@id'}, defaultObj);
        api.setLeadsByUser = $resource(api.URLs.setLeadsByUser, {id: '@id'}, defaultObj);

        api.vehicles = $resource(api.URLs.vehicles, {id: '@id'}, defaultObj);
        api.appraisals = $resource(api.URLs.appraisals, {id: '@id'}, defaultObj);

        api.tasks = $resource(api.URLs.tasks, {id: '@id'}, defaultObj);
        api.taskTypes = $resource(api.URLs.taskTypes, {id: '@id'}, defaultObj);

        api.campaigns = $resource(api.URLs.campaigns, { id: '@id' }, {
            queryAll: queryAll,
            queryAllObj: queryAllObj,
            create: {method: 'POST'},
            update: {
                method: 'PATCH',
                url: 'api/campaigns/:id/'
            },
            getById: {
                method: 'GET',
                url: 'api/campaigns/:id'
            },
            delete: {
                method: 'DELETE',
                url: 'api/campaigns/:id'
            }
        });

        api.concessionaires = $resource(api.URLs.concessionaires, {id: '@id'}, {
            queryAll: queryAll,
            queryAllObj: queryAllObj,
            create: {method: 'POST'},
            update: {method: 'PATCH'},
            removeSource: {
                url:api.URLs.removeSource,
                method: 'DELETE'
            },
            config:{
                url:api.URLs.concessionairesConfig,
                method:'GET'
            }
        });

        api.gasTypes = $resource(api.URLs.gasTypes, {id: '@id'}, defaultObj);

        api.provinces = $resource(api.URLs.provinces, {id: '@id'}, defaultObj);
        api.localities = $resource(api.URLs.localities, {id: '@id'}, defaultObj);
        api.countries = $resource(api.URLs.countries, {id: '@id'}, defaultObj);

        api.brands = $resource(api.URLs.brands, {id: '@id'}, defaultObj);
        api.models = $resource(api.URLs.models, {id: '@id'}, defaultObj);
        api.versions = $resource(api.URLs.versions, {id: '@id'}, defaultObj);

        api.clients = $resource(api.URLs.clients, {id: '@id'}, defaultObj);
        api.businessActivity = $resource(api.URLs.businessActivity, {id: '@id'}, defaultObj);
        api.sectors = $resource(api.URLs.sectors, {id: '@id'}, defaultObj);
        api.whatsapp = $resource(api.URLs.whatsapp, {id: '@id'}, defaultObj);

        api.origins = $resource(api.URLs.origins, {id: '@id'}, defaultObj);

        api.channels = $resource(api.URLs.channels, {id: '@id'}, defaultObj);

        api.sources = $resource(api.URLs.sources, {id: '@id'}, defaultObj);

        api.acds = $resource(api.URLs.acds, {id: '@id'}, {
            queryAll: queryAll,
            queryAllObj: queryAllObj,
            create: {
                url:api.URLs.netelip,
                method: 'POST'
            },
            update: {
                url:api.URLs.netelip,
                method: 'PATCH'
            }
        });

        api.phones = $resource(api.URLs.phones, {id: '@id'}, defaultObj);
        api.emails = $resource(api.URLs.emails, {id: '@id'}, defaultObj);

        api.dashboards = $resource(api.URLs.dashboards, {id: '@id'}, defaultObj);
        api.benchmark = $resource(api.URLs.benchmark, {id: '@id'}, defaultObj);
        api.servicelevel = $resource(api.URLs.servicelevel, {id: '@id'}, defaultObj);
        api.voiceService = $resource(api.URLs.voiceService, {id: '@id'}, defaultObj);
        api.digitalService = $resource(api.URLs.digitalService, {id: '@id'}, defaultObj);

        api.click2calls = $resource(api.URLs.click2calls, {id: '@id'}, defaultObj);

        return api;
    }

})();
