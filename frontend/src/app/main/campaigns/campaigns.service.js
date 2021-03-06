(function () {
    'use strict';

    angular
        .module('app.campaigns')
        .factory('campaignsService', campaignsService);

    function campaignsService($q, api, $http) {

        var service = {
            campaigns: {
                data: [],
                count: 0,
                filters: {
                    startDate: null,
                    endDate: null
                }
            },
            campaign: {},
            getCampaigns: getCampaigns,
            getCampaign: getCampaign,
            saveCampaign: saveCampaign,
            deleteCampaign: deleteCampaign
        }

        return service;

        function deleteCampaign(id) {
            console.log(id);
            var deferred = $q.defer();
            api.campaigns.delete({ id: id }, deleteOk, deleteKO);
            return deferred.promise;

            function deleteOk(response) {
                // Store the clients
                //service.channels.data.push(response);
                //service.channels.count ++;
                deferred.resolve();
            }

            function deleteKO(response) {
                // Actauliza el listado
                //for (var i = 0; i < service.channels.data.length; i++) {
                //    if (service.channels.data[i].id === response.id) {
                //        service.channels.data[i] = angular.copy(response);
                ///    }
                // }
                deferred.reject(response);
            }
        }

        function saveCampaign(data) {
            var deferred = $q.defer();
            var _data = angular.copy(data);
            //_data['concessionaire'] = data['concessionaire']['id'];
            if (_data.id) {
                api.campaigns.update(_data, updateOK, saveKO);
            } else {
                api.campaigns.create(_data, createOK, saveKO);
            }


            function createOK(response) {
                // Store the clients
                //service.channels.data.push(response);
                //service.channels.count ++;
                deferred.resolve(response);
            }

            function updateOK(response) {
                // Actauliza el listado
                //for (var i = 0; i < service.channels.data.length; i++) {
                //    if (service.channels.data[i].id === response.id) {
                //        service.channels.data[i] = angular.copy(response);
                ///    }
                // }
                deferred.resolve(response);
            }

            function saveKO(response) {
                deferred.reject(response);
            }

            return deferred.promise;
        }

        function getCampaign(id) {
            var deferred = $q.defer();
            api.campaigns.getById({ id: id }, getOK, getKO);

            function getOK(response) {
                service.campaign = response;
                const camp = Object.assign(response, {
                    startDate: response['startDate'] ? new Date(response['startDate']) : null,
                    endDate: response['endDate'] ? new Date(response['endDate']) : null
                })
                deferred.resolve(camp);
            }

            function getKO(response) {
                deferred.reject(response);
            }

            return deferred.promise;
        }

        function getCampaigns() {
            var deferred = $q.defer();

            api.campaigns.get(service.campaigns.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                service.campaigns.data = response.results;
                service.campaigns.count = response.count;

                deferred.resolve(service.campaigns);
            }

            function getKO(response) {
                //con esto evitamos que den problemas los not found cuando
                // filtramos y estamos en una p??gina que ya no existe
                if (response.status == 404 && service.campaigns.filters.page != 1) {
                    service.campaigns.filters.page = 1;
                    getChannels();
                }
                deferred.reject(response);
            }
        }
    }

})();