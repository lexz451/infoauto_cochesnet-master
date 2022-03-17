(function () {
    'use strict';
    angular
        .module('app.campaigns')
        .controller('CampaignsController', CampaignsController);

    /** @ngInject */
    function CampaignsController($location, leadsService, originsService, $scope, DebounceService, currentUser, Campaigns, Campaign, Expenses, concessionairesService, campaignsService, vehiclesService, $q) {
        var vm = this;
        vm.currentUser = currentUser;

        vm.campaignStatus = [
            {
                id: 'on',
                name: "Activo"
            },
            {
                id: 'off',
                name: 'Inactivo'
            }
        ]

        vm.campaignTypes = [
            { id: 'type1', name: "Tipo de Campaña #1" },
            { id: 'type2', name: "Tipo de Campaña #2" },
            { id: 'type3', name: "Tipo de Campaña #3" }
        ]

        vm.communicationTypes = [
            { id: 'type1', name: "Tipo de Comunicación #1" },
            { id: 'type2', name: "Tipo de Comunicación #2" },
            { id: 'type3', name: "Tipo de Comunicación #3" }
        ]

        vm.campaigns = Campaigns

        vm.defaultCamp = {
            id: null,
            name: "",
            offer: null,
            concessionaire: null,

            brand: null,
            model: null,
            version: null,
            status: null,
            startDate: null,
            endDate: null
        }

        vm.campaign = Campaign

        vm.expenses = Expenses;

        console.log(Expenses);

        vm.saveCampaign = saveCampaign;
        vm.getConcessionaires = getConcessionaires;
        vm.getBrands = getBrands;
        vm.getModels = getModels;
        vm.getVersions = getVersions;
        vm.getFullNameVersion = getFullNameVersion;
        vm.copyCreate = copyCreate;
        vm.removeCampaign = removeCampaign;
        vm.editCampaign = editCampaign;
        vm.addExpense = addExpense;
        vm.saveExpense = saveExpense;
        vm.deleteExpense = deleteExpense;
        vm.getAllOrigins = getAllOrigins;
        vm.getAllChannels = getAllChannels;
        vm.getLeads = getLeads;
        vm.changeVehicleVersion = changeVehicleVersion;


        $scope.$watch('vm.campaigns.filters', DebounceService(campaignsService.getCampaigns, 300), true);
        $scope.$watch('vm.expenses', getTotalInvestment, true);

        function getTotalInvestment() {
            if (vm.expenses.length) {
                const amount = vm.expenses.map(function(e) {
                    return e.amount;
                }).reduce(function(p,n) {
                    return p + n
                }, 0);
                vm.campaign.investment = amount;
            }
        }

        vm.q = '';

        function getLeads(text) {
            var deferred = $q.defer();
            leadsService.getLeads().then(function (res) {
                console.log(res);
                deferred.resolve(res.data);
            })
            return deferred.promise;
        }

        function getAllChannels(text, origin) {
            var deferred = $q.defer();
            if (origin && origin.available_channels.length > 0) {
                deferred.resolve(origin.available_channels);
            } else {
                deferred.resolve([]);
            }
            return deferred.promise;
        }

        function deleteExpense(i,form) {
            form.$pristine = false;
            vm.expenses.splice(i, 1);
        }

        function addExpense() {
            vm.expenses.push({
                amount: null,
                date: null
            })
        }

        function saveExpense() {
           saveCampaign(vm.campaign);
           campaignsService.getCampaigns();
        }

        function removeCampaign($e, camp) {
            console.log(camp);
            campaignsService.deleteCampaign(camp.id).then(function() {
                campaignsService.getCampaigns().then(function (e) {
                    $location.path('/campaigns/search');
                });
            })
            
        }

        function editCampaign($e, camp) {

        }

        function copyCreate($e, camp) {

        }

        function saveCampaign() {
            const _data = JSON.stringify(vm.expenses);
            vm.campaign.expenses = _data;
            vm.campaign.lead = vm.campaign.lead.id;
            campaignsService.saveCampaign(vm.campaign);
            $location.path('/campaigns/search');
        }

        function validateForm() {

        }

        /* Concesionarios */
        function getConcessionaires(searchText) {
            var deferred = $q.defer();
            concessionairesService.concessionaires.filters = {};
            concessionairesService.concessionaires.filters.search = searchText;
            concessionairesService.concessionaires.filters.page_size = "all";
            concessionairesService.getConcessionaires().then(function (concessionaires) {
                deferred.resolve(concessionaires.data);
            });
            return deferred.promise;
        }

        /* Marcas */
        function getBrands(searchText) {
            var deferred = $q.defer();

            vehiclesService.getBrands(searchText).then(function (brands) {
                deferred.resolve(brands);
            });

            return deferred.promise;
        }

        /* Models */
        function getModels(brand, searchText) {
            var deferred = $q.defer();

            vehiclesService.getModels(brand, searchText).then(function (models) {
                deferred.resolve(models);
            });

            return deferred.promise;
        }

        function getAllOrigins(text) {
            var deferred = $q.defer();
            originsService.getAllOrigins(text).then(function (origins) {
                deferred.resolve(origins);
            });
            return deferred.promise;
        }

        /* Versions */
        function getVersions(model, searchText) {
            var deferred = $q.defer();

            vehiclesService.getVersions(model, searchText).then(function (versions) {
                deferred.resolve(versions);
            });

            return deferred.promise;
        }

        function getFullNameVersion(version) {
            return version.version_name + ' ' + (version.motor || '') + ' ' + (version.engine_power || '');
        }

        /* Change Version */
        function changeVehicleVersion(vehicle, power, gas) {
            /*if (vehicle.version_data) {
                if (vehicle.version_data.engine_power) {
                    vehicle[power] = vehicle.version_data.engine_power;
                }
                if (vehicle.version_data.gas_type_data && vehicle.version_data.gas_type_data.id) {
                    vehicle[gas] = vehicle.version_data.gas_type_data.id;
                }
            }*/
        }

    }
})();