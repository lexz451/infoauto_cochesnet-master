(function () {
    'use strict';
    angular
        .module('app.campaigns')
        .controller('CampaignsController', CampaignsController);

    /** @ngInject */
    function CampaignsController($scope, DebounceService, currentUser, Campaigns, Campaign, Expenses, concessionairesService, campaignsService, vehiclesService, $q) {
        var vm = this;
        vm.currentUser = currentUser;

        vm.campaignStatus = [
            {
                id: 0,
                name: "Status #1"
            }
        ]

        vm.campaignTypes = [
            {
                id: 0,
                name: "Tipo #1"
            }
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
        vm.deleteExpense = deleteExpense;

        $scope.$watch('vm.campaigns.filters', DebounceService(campaignsService.getCampaigns, 300), true);

        vm.q = '';

        function deleteExpense(i) {
            vm.expenses.splice(i, 1);
        }

        function addExpense() {
            vm.expenses.push({
                amount: null,
                date: null
            })
        }

        function removeCampaign($e, camp) {

        }

        function editCampaign($e, camp) {

        }

        function copyCreate($e, camp) {

        }

        function saveCampaign() {
            campaignsService.saveCampaign(vm.campaign);
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
            if (vehicle.version_data) {
                if (vehicle.version_data.engine_power) {
                    vehicle[power] = vehicle.version_data.engine_power;
                }
                if (vehicle.version_data.gas_type_data && vehicle.version_data.gas_type_data.id) {
                    vehicle[gas] = vehicle.version_data.gas_type_data.id;
                }
            }
        }

    }
})();