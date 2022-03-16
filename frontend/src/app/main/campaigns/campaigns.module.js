(function () {
    'use strict';

    angular
        .module('app.campaigns',
            [

            ]
        )
        .config(config);

    /** @ngInject */
    function config($stateProvider) {
        $stateProvider
            .state('app.campaigns', {
                abstract: true,
                url: '/campaigns',
                resolve: {
                    currentUser: function (AuthService) {
                        return AuthService.getCurrentUser().then(function (response) {
                            if (response) {
                                return response;
                            }
                        });
                    },
                    Campaign: function (campaignsService, $stateParams) {
                        return {};
                    }
                }
            })
            .state('app.campaigns.search', {
                url: '/search',
                views: {
                    'content@app': {
                        templateUrl: 'app/main/campaigns/search.html',
                        controller: 'CampaignsController as vm'
                    }
                },
                resolve: {
                    currentUser: function (AuthService) {
                        return AuthService.getCurrentUser().then(function (response) {
                            if (response) {
                                return response;
                            }
                        });
                    },
                    Campaigns: function (campaignsService) {
                        campaignsService.campaigns.filters = {};
                        return campaignsService.getCampaigns();
                    },
                    Campaign: function (campaignsService, $stateParams) {
                        return {};
                    },
                    Expenses: function () {
                        return [];
                    }
                },
                bodyClass: 'todo'
            })
            .state('app.campaigns.edit', {
                url: '/:id',
                views: {
                    'content@app': {
                        templateUrl: 'app/main/campaigns/new.html',
                        controller: 'CampaignsController as vm'
                    }
                },
                resolve: {
                    currentUser: function (AuthService) {
                        return AuthService.getCurrentUser().then(function (response) {
                            if (response) {
                                return response;
                            }
                        });
                    },
                    Campaigns: function (campaignsService) {
                        campaignsService.campaigns.filters = {};
                        return campaignsService.getCampaigns();
                    },
                    Campaign: function (campaignsService, $stateParams) {
                        return campaignsService.getCampaign($stateParams.id);
                    },
                    Expenses: function (Campaign) {
                        const _json = Campaign.expenses;
                        const data = JSON.parse(_json || "[]");
                        return data;
                    }
                    /*Channels: function (channelsService) {
                        channelsService.channels.filters = {};
                        return channelsService.getChannels();
                    }*/
                },
            })
            .state('app.campaigns.new', {
                url: '/new',
                views: {
                    'content@app': {
                        templateUrl: 'app/main/campaigns/new.html',
                        controller: 'CampaignsController as vm'
                    }
                },
                resolve: {
                    currentUser: function (AuthService) {
                        return AuthService.getCurrentUser().then(function (response) {
                            if (response) {
                                return response;
                            }
                        });
                    },
                    Campaigns: function (campaignsService) {
                        campaignsService.campaigns.filters = {};
                        return campaignsService.getCampaigns();
                    },
                    Expenses: function () {
                        return [];
                    }
                    /*Channels: function (channelsService) {
                        channelsService.channels.filters = {};
                        return channelsService.getChannels();
                    }*/
                },
                bodyClass: 'todo'
            });
    }
})();