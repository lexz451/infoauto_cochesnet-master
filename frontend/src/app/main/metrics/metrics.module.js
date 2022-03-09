(function () {
    'use strict';

    angular
        .module('app.metrics',
            [
              'nvd3',
              'gridshore.c3js.chart',
              'angular-chartist'
            ]
        )
        .config(config);

    /** @ngInject */
    function config($stateProvider) {

        $stateProvider
            .state('app.metrics', {
                url: '/metrics',
                views: {
                    'content@app': {
                      templateUrl: 'app/main/metrics/metrics.html',
                      controller: 'MetricsController as vm'
                    }
                },
                resolve:{
                    currentUser: function (AuthService){
                        return AuthService.getCurrentUser().then(function (response) {
                            if (response) {
                                return response;
                            }
                        });
                    },
                    Metrics: function (metricsService) {
                      metricsService.metrics.filters={};
                      metricsService.metrics.filters.user_data=[];
                      return metricsService.metrics;
                    },
                    Benchmark: function (Metrics, metricsService) {
                      return metricsService.benchmark;
                    },
                    Servicelevel: function (Metrics, metricsService) {
                      return metricsService.servicelevel;
                    },
                    VoiceService: function (Metrics, metricsService) {
                      return metricsService.voiceservice;
                    },
                    DigitalService: function (Metrics, metricsService) {
                      return metricsService.digitalservice;
                    }
                },
                bodyClass: 'metrics'
            })
    }
})();
