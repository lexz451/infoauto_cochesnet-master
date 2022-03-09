(function () {
    'use strict';

    angular
        .module('app.leads')
        .controller('LeadEditController', LeadEditController);

    /** @ngInject */
    function LeadEditController($scope, currentUser, Lead, leadsService, $rootScope, provincesService, localitiesService,
        temperaturesService, phonesService, qualificationsService, scoresService, taskTypesService,
        sourcesService, $document, $stateParams, GasTypes, Tasks, tasksService, Concessionaire,
        clientsService, emailsService, $state, NotifyService, $mdDialog, $q, acdsService, $timeout,
        Source, click2callsService, LeadsIncomingCalls, LeadsOutgoingCalls, LeadsHistory, channelsService,
        vehiclesService, appraisalsService, usersService, LeadsActivity, originsService, gettextCatalog,
        leadResultsService, leadActionsService, StartCall, leadStatusService, $sce, concessionairesService,
        LeadsNews, LeadsAttended, LeadsCommercialManagements, LeadsTracings, LeadsEnds, DebounceService) {
        var vm = this;

        // Data
        vm.user = currentUser;
        vm.lead = angular.copy(Lead);
        vm.tasks = Tasks;
        vm.leadStatus = leadStatusService.leadStatus;
        vm.isOpenFinishLeadBox = false;
        vm.concessionaire = Concessionaire;
        vm.origins = [];
        vm.iframeAdLink = null;

        vm.clientTypes = [
            { id: 'private', name: 'Particular' },
            { id: 'freelance', name: 'Autonomo' },
            { id: 'company', name: 'Empresa' }
        ]

        vm.clientSegments = [
            { id: 'tur', name: "Turismo" },
            { id: 'comercial', name: "Comercial" },
            { id: 'moto', name: "Motocicleta" },
            { id: 'other', name: "Otro" },
        ]

        vm.vehiclePurchaseMethods = [
            { id: 'count', name: "Contado" },
            { id: 'rent', name: "Renting" },
            { id: 'lease', name: 'Leasing' },
            { id: 'fin', name: 'Financiacion' }
        ]

        vm.leadStatuses = [
            { id: 'new', name: "Leads no atendidos" },
            { id: 'attended', name: "Leads atendidos por Comercial/Cualificado" },
            { id: 'commercial_management', name: 'Tareas pendientes' },
            { id: 'tracing', name: 'Seguimiento' },
            { id: 'end', name: 'Leads cerrados' }
        ]


        vm.vehicleFinancialTerms = [
            { id: 3, name: 3 }, { id: 6, name: 6 },
            { id: 9, name: 9 }, { id: 12, name: 12 }, { id: 15, name: 15 }, { id: 18, name: 18 }, { id: 21, name: 21 }, { id: 24, name: 24 }, { id: 27, name: 27 }, { id: 30, name: 30 }, { id: 33, name: 33 }, { id: 36, name: 36 }, { id: 39, name: 39 }, { id: 42, name: 42 }, { id: 45, name: 45 }, { id: 48, name: 48 },
            { id: 51, name: 51 }, { id: 54, name: 54 }, { id: 57, name: 57 }, { id: 60, name: 60 }, { id: 63, name: 63 }, { id: 66, name: 66 }, { id: 69, name: 69 }, { id: 72, name: 72 },
            { id: 75, name: 75 }, { id: 78, name: 78 }, { id: 81, name: 81 }, { id: 84, name: 84 }, { id: 87, name: 87 }, { id: 90, name: 90 }, { id: 93, name: 93 }, { id: 96, name: 96 },
            { id: 99, name: 99 }, { id: 102, name: 102 }, { id: 105, name: 105 }, { id: 108, name: 108 }, { id: 111, name: 111 }, { id: 114, name: 114 }, { id: 117, name: 117 }, { id: 120, name: 120 }
        ]

        // Data BOARD
        vm.board = {
            lists: [
                { id: 'new', name: gettextCatalog.getString('Leads no atendidos'), show: true },
                { id: 'attended', name: gettextCatalog.getString('Leads atendidos por Comercial/Cualificado'), show: true },
                { id: 'commercial_management', name: gettextCatalog.getString('Tareas pendientes'), show: true },
                { id: 'tracing', name: gettextCatalog.getString('Seguimiento'), show: true },
                { id: 'end', name: gettextCatalog.getString('Leads cerrados'), show: true }
            ]
        };

        vm.leads = {
            new: LeadsNews,
            attended: LeadsAttended,
            commercial_management: LeadsCommercialManagements,
            tracing: LeadsTracings,
            end: LeadsEnds,
        };

        vm.filters = {}

        // Watchers
        $scope.$watch('vm.leads.new.filters', DebounceService(leadsService.getLeadsNews, 300), true);
        $scope.$watch('vm.leads.attended.filters', DebounceService(leadsService.getLeadsAttended, 300), true);
        $scope.$watch('vm.leads.commercial_management.filters', DebounceService(leadsService.getLeadsCommercialManagements, 300), true);
        $scope.$watch('vm.leads.tracing.filters', DebounceService(leadsService.getLeadsTracings, 300), true);
        $scope.$watch('vm.leads.end.filters', DebounceService(leadsService.getLeadsEnds, 300), true);

        $scope.$watch('vm.leads.new.data', DebounceService(openDuplicateLeadsDialog, 300), true);
        $scope.$watch('vm.leads.attended.data', DebounceService(openDuplicateLeadsDialog, 300), true);
        $scope.$watch('vm.leads.commercial_management.data', DebounceService(openDuplicateLeadsDialog, 300), true);
        $scope.$watch('vm.leads.tracing.data', DebounceService(openDuplicateLeadsDialog, 300), true);
        $scope.$watch('vm.leads.end.data', DebounceService(openDuplicateLeadsDialog, 300), true);
        // END DATA BOARD

        vm.leadAction = leadActionsService.getEmptyLeadAction(Lead);
        vm.leadsIncomingCalls = LeadsIncomingCalls;
        vm.leadsOutgoingCalls = LeadsOutgoingCalls;
        vm.leadsHistory = {
            dataToday: {},
            dataYesterday: {},
            dataOthers: {},
            count: 0
        };
        vm.histories = [
            {
                title: gettextCatalog.getString("Hoy"),
                key: 'dataToday'
            },
            {
                title: gettextCatalog.getString("Ayer"),
                key: 'dataYesterday'
            },
            {
                title: gettextCatalog.getString("Anteriormente"),
                key: 'dataOthers'
            }
        ];
        vm.leadsActivity = {
            dataFuture: {},
            dataToday: {},
            dataYesterday: {},
            dataOthers: {},
            count: 0
        };
        vm.activities = [
            {
                title: gettextCatalog.getString("Próximamente"),
                key: 'dataFuture'
            },
            {
                title: gettextCatalog.getString("Hoy"),
                key: 'dataToday'
            },
            {
                title: gettextCatalog.getString("Ayer"),
                key: 'dataYesterday'
            },
            {
                title: gettextCatalog.getString("Anteriormente"),
                key: 'dataOthers'
            }
        ];

        vm.temperatures = temperaturesService.temperatures;
        vm.qualifications = qualificationsService.qualifications;
        vm.scores = scoresService.scores;
        vm.taskTypes = [];
        taskTypesService.getTaskTypes(false).then(function (res) {
            vm.taskTypes = res;
            taskTypesService.getTaskTypes(true).then(function (res) {
                vm.taskTypes = vm.taskTypes.concat(res);
            });
        });
        vm.gasTypes = GasTypes;

        vm.results = leadResultsService.newLeadResults;
        vm.resultReasons = leadResultsService.resultReasons;

        vm.vehicleTypes = [
            { id: 'new', name: gettextCatalog.getString('Nuevo') },
            { id: 'km0', name: gettextCatalog.getString('Km0') },
            { id: 'seminew', name: gettextCatalog.getString('Seminuevo') },
            { id: 'used', name: gettextCatalog.getString('Ocasión') }
        ];
        vm.comercialCategories = [
            { id: 'request_product', name: gettextCatalog.getString('Producto solicitado') },
            { id: 'offered_product', name: gettextCatalog.getString('Producto ofertado') },
        ];
        vm.requestTypes = [
            { id: 'new', name: gettextCatalog.getString('Nuevo') },
            { id: 'km0', name: gettextCatalog.getString('Kilometro 0') },
            { id: 'seminew', name: gettextCatalog.getString('Seminuevo') },
            { id: 'used', name: gettextCatalog.getString('Ocasión') },
            { id: 'management', name: gettextCatalog.getString('Gerencia') },
            { id: 'apv', name: gettextCatalog.getString('Postventa') },
            { id: 'acc', name: gettextCatalog.getString('Accesorios') }
        ];

        vm.gearShifts = [
            { id: 'manual', name: gettextCatalog.getString('Manual') },
            { id: 'auto', name: gettextCatalog.getString('Automático') }
        ];

        if ($stateParams.source) {
            vm.lead.source_data = Source;
            vm.lead.source_data_prov = Source;
            vm.lead.concessionaire_data = Source.concession_data;
        }

        if ($stateParams.phone) {
            vm.lead.client.phone = $stateParams.phone;
        }

        if ($stateParams.user) {
            vm.lead.user = $stateParams.user;
            usersService.getUser(vm.lead.user).then(function (user) {
                vm.lead.user_data = user;
            });
        }

        vm.week = {};
        vm.week.monday = gettextCatalog.getString("Lunes");
        vm.week.tuesday = gettextCatalog.getString("Martes");
        vm.week.wednesday = gettextCatalog.getString("Miércoles");
        vm.week.thursday = gettextCatalog.getString("Jueves");
        vm.week.friday = gettextCatalog.getString("Viernes");
        vm.week.saturday = gettextCatalog.getString("Sábado");
        vm.week.sunday = gettextCatalog.getString("Domingo");

        $scope.$on('$stateChangeStart', function (event, toState, toParams, fromState, fromParams) {
            if (fromState.name === "app.leads.get.edit") {

                if ($scope.leadForm.$dirty) {
                    event.preventDefault();

                    var confirm = $mdDialog.confirm()
                        .title(gettextCatalog.getString('Se han detectado cambios'))
                        .textContent(gettextCatalog.getString('Si abandona esta pantalla perderá los cambios, ¿Desea guardar los cambios?'))
                        .ariaLabel(gettextCatalog.getString('Guardar lead'))
                        .clickOutsideToClose(true)
                        .parent(angular.element(document.body))
                        .ok(gettextCatalog.getString('Guardar'))
                        .cancel(gettextCatalog.getString('Abandonar'));

                    $mdDialog.show(confirm).then(function () {
                        openSaveLeadDialog();
                    }, function (error) {
                        $scope.leadForm.$setPristine();
                        $state.go(toState.name, { lead: 0 });
                    });
                }
            }
        });

        init();

        // Watchers
        $scope.$watch('vm.lead.client_data', function (n, o) {
            if (n && (!o || n.id !== o.id)) {
                vm.lead.client = n;
            }
        }, true);

        // Methods
        vm.canEdit = canEdit;
        vm.isDisabled = isDisabled;
        vm.openSaveLeadDialog = openSaveLeadDialog;
        vm.saveLead = saveLead;
        vm.changeStatus = changeStatus;
        vm.finishLead = finishLead;
        vm.saveAndfinishLead = saveAndfinishLead;
        vm.addNote = addNote;
        vm.deleteNote = deleteNote;
        vm.addTag = addTag;
        vm.deleteTag = deleteTag;
        vm.openTaskDialog = openTaskDialog;
        vm.removeTask = removeTask;
        vm.getProvinces = getProvinces;
        vm.getLocalities = getLocalities;
        vm.getBrands = getBrands;
        vm.getModels = getModels;
        vm.getVersions = getVersions;
        vm.getFullNameVersion = getFullNameVersion;
        vm.changeVehicleVersion = changeVehicleVersion;
        vm.getBusinessActivity = getBusinessActivity;
        vm.getSectors = getSectors;
        vm.sendWhatsapp = sendWhatsapp;
        vm.completeAddress = completeAddress;
        vm.getConcessionaires = getConcessionaires;
        vm.getOrigins = getOrigins;
        vm.getAllOrigins = getAllOrigins;
        vm.getChannels = getChannels;
        vm.getAllChannels = getAllChannels;
        vm.changeChannel = changeChannel;
        vm.getExposicion = getExposicion;
        vm.getSources = getSources;
        vm.getFullNamceSource = getFullNamceSource;
        vm.getFullUserName = getFullUserName;
        vm.getClients = getClients;
        vm.openLeadDialog = openLeadDialog;
        vm.openLeadContactDialog = openLeadContactDialog;
        vm.openLeadStatusDialog = openLeadStatusDialog;
        vm.openLeadStatusDateDialog = openLeadStatusDateDialog;
        vm.getLastRealizationDate = getLastRealizationDate;
        vm.datediff = datediff;
        vm.eventClientBlur = eventClientBlur;
        vm.eventClientEmailBlur = eventClientEmailBlur;
        vm.setExtension = setExtension;
        vm.call = call;
        vm.objectSize = objectSize;
        vm.openLeadHistoryDialog = openLeadHistoryDialog;
        vm.openLeadActivityDialog = openLeadActivityDialog;
        vm.addVehicle = addVehicle;
        vm.deleteVehicle = deleteVehicle;
        vm.addAppraisal = addAppraisal;
        vm.deleteAppraisal = deleteAppraisal;
        vm.changeSource = changeSource;
        vm.selectOrigin = selectOrigin;
        vm.getNumber = getNumber;
        vm.saveTask = saveTask;
        vm.reactivate = reactivate;
        vm.sendMail = sendMail;
        vm.trustSrc = trustSrc;
        vm.hubspot = hubspot;

        //////////
        function init() {
            for (var i in LeadsHistory.data) {
                //elegimos si vamos a añadirlo a hoy, ayer o anteriormente
                var key = getKeyHistory(LeadsHistory.data[i]);

                if (!vm.leadsHistory[key][LeadsHistory.data[i].history_user]) {
                    vm.leadsHistory[key][LeadsHistory.data[i].history_user] = {
                        data: [],
                        count: 0,
                        history_date_start: LeadsHistory.data[i].history_date,
                        history_date_end: LeadsHistory.data[i].history_date,
                        history_user: LeadsHistory.data[i].history_user
                    };
                }
                vm.leadsHistory.count++;
                vm.leadsHistory[key][LeadsHistory.data[i].history_user].data.push(LeadsHistory.data[i]);
                vm.leadsHistory[key][LeadsHistory.data[i].history_user].count++;
                vm.leadsHistory[key][LeadsHistory.data[i].history_user].history_date_start = LeadsHistory.data[i].history_date;
            }

            for (var i in LeadsActivity.data) {
                //elegimos si vamos a añadirlo a hoy, ayer o anteriormente
                var key = getKeyActivity(LeadsActivity.data[i]);

                if (!vm.leadsActivity[key][LeadsActivity.data[i].user]) {
                    vm.leadsActivity[key][LeadsActivity.data[i].user] = {
                        data: [],
                        count: 0,
                        activity_date_start: LeadsActivity.data[i].date,
                        activity_date_end: LeadsActivity.data[i].date,
                        activity_user: LeadsActivity.data[i].user_data
                    };
                }
                vm.leadsActivity.count++;
                vm.leadsActivity[key][LeadsActivity.data[i].user].data.push(LeadsActivity.data[i]);
                vm.leadsActivity[key][LeadsActivity.data[i].user].count++;
                vm.leadsActivity[key][LeadsActivity.data[i].user].activity_date_start = LeadsActivity.data[i].date;
            }

            //cargamos los orígenes disponbiles
            if (vm.lead.id && vm.lead.concessionaire) {
                reloadOrigins(vm.lead.concessionaire);
            }

            if (StartCall) {
                call(vm.lead);
            }


        }

        function reloadOrigins(concessionaire) {
            originsService.origins.filters.source__concession = concessionaire;
            originsService.getAllOrigins().then(function (res) {
                vm.origins = res;
                reloadLead(vm.lead);
            });
        }

        function getKeyHistory(history) {
            var date = moment(history.history_date).format("DD-MM-YYYY");
            var today = moment().format("DD-MM-YYYY");
            var yesterday = moment().subtract(1, 'd').format('DD-MM-YYYY');

            if (date === today) {
                return "dataToday";
            } else if (date === yesterday) {
                return "dataYesterday";
            }
            return "dataOthers";
        }

        function getKeyActivity(activity) {
            var date = moment(activity.date).format("DD-MM-YYYY");
            var today = moment().format("DD-MM-YYYY");
            var yesterday = moment().subtract(1, 'd').format('DD-MM-YYYY');

            if (date === today) {
                return "dataToday";
            } else if (date === yesterday) {
                return "dataYesterday";
            } else if (validate_fechaMayorQue(today, date)) {
                return "dataFuture";
            }
            return "dataOthers";
        }

        function validate_fechaMayorQue(fechaInicial, fechaFinal) {
            var valuesStart = fechaInicial.split("-");
            var valuesEnd = fechaFinal.split("-");

            // Verificamos que la fecha no sea posterior a la actual
            var dateStart = new Date(valuesStart[2], (valuesStart[1] - 1), valuesStart[0]);
            var dateEnd = new Date(valuesEnd[2], (valuesEnd[1] - 1), valuesEnd[0]);
            return !(dateStart >= dateEnd);
        }

        function objectSize(obj) {
            var size = 0, key;
            for (key in obj) {
                if (obj.hasOwnProperty(key)) size++;
            }
            return size;
        }

        function canEdit() {
            if (!vm.lead.id || vm.lead.status === 'new' || vm.lead.status === 'pending') {
                return true
            }
            if (vm.user.id = vm.lead.user || vm.user.is_admin) {
                return true
            }
            return false;
        }

        function isDisabled() {
            /*if (vm.lead.status === 'end') {
                return true;
            }*/
            return false;
        }

        function reloadLead(lead) {
            for (var i in lead) {
                if (i !== 'source_data' && i !== 'concessionaire_data' && i !== 'origin2_data') {
                    vm.lead[i] = lead[i];
                }
            }
            if (!vm.lead.source_data_prov && vm.lead.source_data) {
                vm.lead.source_data_prov = vm.lead.source_data;
                vm.lead.source = null;
            }

            for (var i in vm.lead.vehicles) {
                selectOrigin(vm.lead.vehicles[i]);

                if (vm.lead.vehicles[i].brand_model) {
                    vm.lead.vehicles[i].brand_model_data = {
                        id: vm.lead.vehicles[i].brand_model.split("___")[1] || null,
                        name: vm.lead.vehicles[i].brand_model.split("___")[0],
                    }
                }

                if (vm.lead.vehicles[i].model) {
                    vm.lead.vehicles[i].model_data = {
                        id: vm.lead.vehicles[i].model.split("___")[1] || null,
                        model_name: vm.lead.vehicles[i].model.split("___")[0],
                    }
                }

                if (vm.lead.vehicles[i].version) {
                    vm.lead.vehicles[i].version_data = {
                        id: vm.lead.vehicles[i].version.split("___")[1] || null,
                        version_name: vm.lead.vehicles[i].version.split("___")[0],
                    }
                }
            }

            for (var i in vm.lead.appraisals) {
                if (vm.lead.appraisals[i].brand) {
                    vm.lead.appraisals[i].brand_data = {
                        id: vm.lead.appraisals[i].brand.split("___")[1] || null,
                        name: vm.lead.appraisals[i].brand.split("___")[0],
                    }
                }

                if (vm.lead.appraisals[i].model) {
                    vm.lead.appraisals[i].model_data = {
                        id: vm.lead.appraisals[i].model.split("___")[1] || null,
                        model_name: vm.lead.appraisals[i].model.split("___")[0],
                    }
                }

                if (vm.lead.appraisals[i].version) {
                    vm.lead.appraisals[i].version_data = {
                        id: vm.lead.appraisals[i].version.split("___")[1] || null,
                        version_name: vm.lead.appraisals[i].version.split("___")[0],
                    }
                }
            }

            if (vm.lead.vehicles && vm.lead.vehicles[0] && vm.lead.vehicles[0].ad_link) {
                vm.iframeAdLink = vm.lead.vehicles[0].ad_link
            }

            for (var i in vm.lead.appraisals) {
                vm.lead.appraisals[i].circulation_date = vm.lead.appraisals[i].circulation_date ? new Date(moment(vm.lead.appraisals[i].circulation_date).format()) : null;
                vm.lead.appraisals[i].buy_date = vm.lead.appraisals[i].buy_date ? new Date(moment(vm.lead.appraisals[i].buy_date).format()) : null;
                vm.lead.appraisals[i].registration_date = vm.lead.appraisals[i].registration_date ? new Date(moment(vm.lead.appraisals[i].registration_date).format()) : null;
                vm.lead.appraisals[i].last_mechanic_date = vm.lead.appraisals[i].last_mechanic_date ? new Date(moment(vm.lead.appraisals[i].last_mechanic_date).format()) : null;
            }
        }

        function cleanLead(lead) {
            var deleteVars = [];
            for (var i in lead) {
                if (i.indexOf('$') >= 0) {
                    deleteVars.push(i);
                } else if (typeof lead[i] == 'object') {
                    cleanLead(lead[i]);
                }
            }
            for (var i in deleteVars) {
                delete lead[deleteVars[i]];
            }
            if (lead && lead.vehicles) {
                for (var i in lead.vehicles) {
                    delete lead.vehicles[i].field;
                }
            }
        }

        function openSaveLeadDialog() {
            vm.leadAction.date = undefined;

            return saveLead(false).then(function (response) {
                $scope.leadForm.$setPristine();
                reloadLead(response);

                for (var i = 0; i < response.request.task.length; i++) {
                    if (!vm.leadAction.date && new Date() <= moment(response.request.task[i].planified_realization_date)) {
                        vm.leadAction.date = moment(response.request.task[i].planified_realization_date);
                    }

                    if (moment(response.request.task[i].planified_realization_date) < vm.leadAction.date && new Date() <= vm.leadAction.date) {
                        vm.leadAction.date = moment(response.request.task[i].planified_realization_date)
                    }
                }

                vm.leadAction.lead = response.id;
                vm.leadAction.lead_status_planing = response.status;

                if (vm.leadAction.date) {
                    leadActionsService.saveLeadAction(vm.leadAction).then(function (response) {
                        $timeout(function () {
                            $state.go("app.leads.board");
                        }, 500);
                        NotifyService.successMessage(gettextCatalog.getString("Lead guardado correctamente"));

                    }, function (error) {
                        vm.serverErrors = error.data;
                        console.log($scope.leadForm)
                        NotifyService.errorMessage(gettextCatalog.getString("Error al guardar el Lead.") + " " + (error.data.non_field_errors || ""));
                    });
                }
            });

        }


        /**
         * Guardar detalle del informe
         */

        function saveLead(redirect) {
            redirect = typeof redirect !== 'undefined' ? redirect : true;
            var deferred = $q.defer();

            var lead = angular.copy(vm.lead);
            if (lead.id) {
                delete lead.request;
            }

            var err = {};
            if (!lead.concessionaire_data || !lead.concessionaire_data.id) {
                err.concessionaire = ["Este campo es requerido."];
            }
            if (!lead.source_data || !lead.source_data.origin_data || !lead.source_data.origin_data.id) {
                err.origin = ["Este campo es requerido."];
            }
            if (!lead.source_data || !lead.source_data.channel_data || !lead.source_data.channel_data.id) {
                err.channel = ["Este campo es requerido."];
            }
            if (!lead.source_data_prov || !lead.source_data_prov.id) {
                err.source = ["Este campo es requerido."];
            }
            if (err.concessionaire || err.origin || err.channel || err.source) {
                vm.serverErrors = err;
                NotifyService.errorMessage(gettextCatalog.getString("Error al guardar el informe."));
                deferred.reject(err);
                return deferred.promise;
            }

            if (lead.origin2_data && lead.origin2_data.id) {
                lead.origin2 = lead.origin2_data.id;
            } else {
                lead.origin2 = null;
            }

            if (lead.channel2_data && lead.channel2_data.id) {
                lead.channel2 = lead.channel2_data.id;
            } else {
                lead.channel2 = null;
            }
            delete lead.status;

            if (vm.lead.request.task.length < 1) {
                var confirm = $mdDialog.confirm()
                    .title(gettextCatalog.getString('Guardar lead'))
                    .textContent(gettextCatalog.getString('Este lead no tiene ninguna solicitud adjunta. ¿Desea continuar?'))
                    .ariaLabel(gettextCatalog.getString('Guardar lead'))
                    .clickOutsideToClose(true)
                    .parent(angular.element(document.body))
                    .ok(gettextCatalog.getString('Continuar'))
                    .cancel(gettextCatalog.getString('Cancelar'));

                $mdDialog.show(confirm).then(function () {
                    leadsService.saveLead(lead).then(function (response) {
                        if ($stateParams.acd) {
                            var obj = {
                                call_control: $stateParams.acd,
                                lead: response.id,
                            };
                            acdsService.saveAcd(obj);
                        }

                        reloadLead(response);
                        if (redirect) {
                            $state.go("app.leads.board");
                        }
                        $rootScope.loadingProgress = false;
                        NotifyService.successMessage(gettextCatalog.getString("Informe guardado correctamente"));
                        vm.serverErrors = null;
                        deferred.resolve(response);
                    }, function (error) {
                        console.log(error);
                        $rootScope.loadingProgress = false;
                        vm.serverErrors = error.data;
                        NotifyService.errorMessage(gettextCatalog.getString("Error al guardar el informe.") + " " + (error.data.non_field_errors || ""));
                        deferred.reject(error);
                    });
                }, function () {
                    $rootScope.loadingProgress = false;
                    deferred.reject();
                });
            } else {
                leadsService.saveLead(lead).then(function (response) {
                    if ($stateParams.acd) {
                        var obj = {
                            id: $stateParams.acd,
                            lead: response.id,
                        };
                        acdsService.saveAcd(obj);
                    }

                    reloadLead(response);
                    if (redirect) {
                        $state.go("app.leads.board");
                    }
                    $rootScope.loadingProgress = false;
                    NotifyService.successMessage(gettextCatalog.getString("Informe guardado correctamente"));
                    vm.serverErrors = null;
                    deferred.resolve(response);
                }, function (error) {
                    vm.serverErrors = error.data;
                    $rootScope.loadingProgress = false;
                    NotifyService.errorMessage(gettextCatalog.getString("Error al guardar el informe.") + " " + (error.data.non_field_errors || ""));
                    deferred.reject(error);
                });
            }

            return deferred.promise;
        }

        /**
         * Modifica el stado del informe
         */
        function changeStatus(lead, status) {
            if (lead.id) {
                var obj = {
                    status: status,
                    id: lead.id
                };
                var oldStatus = lead.status;
                lead.status = status;

                return leadsService.saveLead(obj).then(function (res) {
                    NotifyService.successMessage(gettextCatalog.getString("Acción realizada correctamente"));
                    vm.lead.status_dates = res.status_dates;
                    vm.lead.status_new_datetime = res.status_new_datetime;
                    vm.lead.status_pending_datetime = res.status_pending_datetime;
                    vm.lead.status_attended_datetime = res.status_attended_datetime;
                    vm.lead.status_tracing_datetime = res.status_tracing_datetime;
                    vm.lead.status_end_datetime = res.status_end_datetime;
                }, function (error) {
                    lead.status = oldStatus;
                    vm.serverErrors = error.data;
                    NotifyService.errorMessage(gettextCatalog.getString("Error al realizar la acción.") + " " + (error.data.non_field_errors || ""));
                });
            } else {
                //PARA LA CREACCION
                vm.lead.status = status;
                vm.lead.status_dates = {};
                vm.lead.status_dates[status] = new Date();
            }
        }

        /**
         * Finaliza el informe
         */
        function finishLead() {
            var deferred = $q.defer();
            leadsService.getLead(vm.lead.id).then(function (res) {
                if (res.pending_tasks) {
                    var confirm = $mdDialog.confirm()
                        .title(gettextCatalog.getString('Finalizar lead'))
                        .textContent(gettextCatalog.getString('Tienes tareas pendientes de realización y seguimiento ¿Estás seguro de querer finalizar el lead?'))
                        .ariaLabel(gettextCatalog.getString('Finalizar lead'))
                        .clickOutsideToClose(true)
                        .parent(angular.element(document.body))
                        .ok(gettextCatalog.getString('Confirmar'))
                        .cancel(gettextCatalog.getString('Cancelar'));

                    $mdDialog.show(confirm).then(function () {
                        //Abrimos el modal de resultados de gestion
                        openFinishLeadBox();
                    });
                } else {
                    //Abrimos el modal de resultados de gestion
                    openFinishLeadBox();
                }
                deferred.resolve();
            }, function () {
                deferred.reject();
            });
            return deferred.promise;
        }

        /**
         * Guarda y Finaliza el informe
         */
        function saveAndfinishLead() {
            var deferred = $q.defer();
            var redirect = false;
            vm.saveLead(redirect).then(function (response) {
                leadsService.getLead(response.id).then(function (res) {
                    if (res.pending_tasks) {
                        var confirm = $mdDialog.confirm()
                            .title(gettextCatalog.getString('Finalizar lead'))
                            .textContent(gettextCatalog.getString('Tienes tareas pendientes de realización y seguimiento ¿Estás seguro de querer finalizar el lead?'))
                            .ariaLabel(gettextCatalog.getString('Finalizar lead'))
                            .clickOutsideToClose(true)
                            .parent(angular.element(document.body))
                            .ok(gettextCatalog.getString('Confirmar'))
                            .cancel(gettextCatalog.getString('Cancelar'));

                        $mdDialog.show(confirm).then(function () {
                            //Abrimos el modal de resultados de gestion
                            openFinishLeadBox();
                        });
                    } else {
                        //Abrimos el modal de resultados de gestion
                        openFinishLeadBox();
                    }
                    deferred.resolve();
                }, function () {
                    deferred.reject();
                })
            }, function () {
                deferred.reject();
            });
            return deferred.promise;
        }

        /**
         * Abre el dialogo para indicar el resultado del lead
         */
        function openFinishLeadDialog(lead) {
            lead = typeof lead !== 'undefined' ? lead : vm.lead;
            $mdDialog.show({
                controller: 'FinishLeadDialogController',
                controllerAs: 'vm',
                templateUrl: 'app/main/leads/dialogs/finishLead/finishLead-dialog.html',
                parent: angular.element($document.body),
                clickOutsideToClose: true,
                locals: {
                    Lead: lead
                }
            });
        }

        /**
         * Muestra el cuadro con las opciones de cierre de lead
         */
        function openFinishLeadBox() {
            vm.isOpenFinishLeadBox = true;
            /*vm.lead={
                result:null,
                result_reason:null,
                id:Lead.id
            };*/

        }

        /**
         * Añade una nota
         */
        function addNote() {
            vm.lead.note.push({ content: '', modified: new Date() });
        }

        /**
         * borra una nota
         */
        function deleteNote(note) {
            if (note.id) {
                //buscamos por id
                for (var i = 0; i < vm.lead.note.length; i++) {
                    if (vm.lead.note[i].id === note.id) {
                        vm.lead.note.splice(i, 1);
                        break;
                    }
                }
            } else {
                //buscamos por contenido
                for (var i = 0; i < vm.lead.note.length; i++) {
                    if (vm.lead.note[i].content === note.content && !note.id) {
                        vm.lead.note.splice(i, 1);
                        break;
                    }
                }
            }
        }

        /**
         * Añade un tag
         */
        function addTag() {
            vm.lead.tags.push({ content: '', modified: new Date() });
        }

        /**
         * borra un tag
         */
        function deleteTag(tag) {
            if (tag.id) {
                //buscamos por id
                for (var i = 0; i < vm.lead.tags.length; i++) {
                    if (vm.lead.tags[i].id === tag.id) {
                        vm.lead.tags.splice(i, 1);
                        break;
                    }
                }
            } else {
                //buscamos por contenido
                for (var i = 0; i < vm.lead.tags.length; i++) {
                    if (vm.lead.tags[i].content === tag.content && !tag.id) {
                        vm.lead.tags.splice(i, 1);
                        break;
                    }
                }
            }
        }

        /**
         * Abre el dialogo para crear/editar una tarea
         *
         * @param ev
         * @param task
         */
        function openTaskDialog(ev, tracing, task) {
            if (!vm.lead.id) {
                $rootScope.loadingProgress = true;
                leadsService.saveLead(vm.lead).then(function (response) {
                    vm.lead.id = response.id;
                    vm.lead.request = response.request;
                    vm.openTaskDialog(ev, tracing, task);
                    $rootScope.loadingProgress = false;
                }, function (error) {
                    $rootScope.loadingProgress = false;
                    vm.serverErrors = error.data;
                    NotifyService.errorMessage(gettextCatalog.getString("Error al guardar el informe.") + " " + (error.data.non_field_errors || ""));
                });
                return;
            }

            if (task) task.datetime = new Date(task.planified_realization_date)
            $mdDialog.show({
                controller: 'TaskDialogController',
                controllerAs: 'vm',
                templateUrl: 'app/main/tasks/dialogs/task/task-dialog.html',
                parent: angular.element($document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                locals: {
                    Task: task,
                    Tracing: tracing,
                    GasTypes: GasTypes,
                    Request: vm.lead.request,
                    Lead: vm.lead.id,
                    event: ev
                }
            });
        }

        /**
         * Abre el dialogo para eliminar una task
         *
         * @param ev
         * @param task
         */
        function removeTask(ev, task) {
            var confirm = $mdDialog.confirm()
                .title(gettextCatalog.getString('Eliminar solicitud'))
                .textContent(gettextCatalog.getString('¿Seguro que quieres eliminar la solicitud?'))
                .ariaLabel(gettextCatalog.getString('Eliminar solicitud'))
                .clickOutsideToClose(true)
                .parent(angular.element(document.body))
                .ok(gettextCatalog.getString('Borrar solicitud'))
                .cancel(gettextCatalog.getString('Cancelar'));

            $mdDialog.show(confirm).then(function () {
                tasksService.removeTask(task).then(function () {
                    NotifyService.successMessage(gettextCatalog.getString("Solicitud borrada correctamente."));
                }, function (error) {
                    NotifyService.errorMessage(gettextCatalog.getString("Error al borrar la solicitud.") + " " + (error.data.detail || ""));
                });
            });

        }

        function createFilterFor(query) {
            var lowercaseQuery = getCleanedString(query);
            return function filterFn(q) {
                return (getCleanedString(q.name || q.data).includes(lowercaseQuery));
            };
        }

        /* Provincias */
        function getProvinces(searchText) {
            var deferred = $q.defer();
            // El id de españa es el 28
            provincesService.getProvinces("28", searchText).then(function (provinces) {
                var results = searchText ? provinces.filter(createFilterFor(searchText)) : provinces;
                deferred.resolve(results);
            });

            return deferred.promise;
        }

        /* Localidades */
        function getLocalities(searchText) {
            var deferred = $q.defer();
            var province = null;
            if (vm.lead.client.province_data) {
                province = vm.lead.client.province_data.id;
            }
            localitiesService.getLocalities(province, searchText).then(function (localities) {
                var results = searchText ? localities.filter(createFilterFor(searchText)) : localities;
                deferred.resolve(results);
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

        /* Send Whatsapp */
        function sendWhatsapp(ev) {
            $mdDialog.show({
                controller: 'SendWhatsappDialogController',
                controllerAs: 'vm',
                templateUrl: 'app/main/leads/dialogs/sendWhatsapp/sendWhatsapp-dialog.html',
                parent: angular.element($document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                locals: {
                    Lead: vm.lead,
                    event: ev
                }
            })
        }

        /* Sectors */
        function getSectors(searchText) {
            var deferred = $q.defer();

            clientsService.getSectors(searchText).then(function (sectors) {
                deferred.resolve(sectors);
            });

            return deferred.promise;
        }

        /* Business Activity */
        function getBusinessActivity(sector, searchText) {
            var deferred = $q.defer();

            clientsService.getBusinessActivity(sector, searchText).then(function (activities) {
                deferred.resolve(activities);
            });

            return deferred.promise;
        }

        /* Autocompleta Provincias y Localidades */
        function completeAddress() {
            localitiesService.getLocalitiesByCodPostal(vm.lead.client.postal_code).then(function (localities) {
                console.log(localities);
                if (localities && localities[0]) {
                    vm.lead.client.location_data = localities[0];
                    vm.lead.client.province_data = localities[0].province;
                }
            });
        }

        /* Concesionarios */
        function getConcessionaires(searchText) {
            var deferred = $q.defer();
            if (vm.lead.user_data && vm.lead.user_data.id) {
                usersService.getUser(vm.lead.user_data.id).then(function (user) {
                    var concessionaires = user.related_concessionaires.map(function (related_concessionaire) {
                        return related_concessionaire.concessionaire_data;
                    });
                    var results = searchText ? concessionaires.filter(createFilterFor(searchText)) : concessionaires;
                    deferred.resolve(results);
                });
            } else {
                concessionairesService.concessionaires.filters = {};
                concessionairesService.concessionaires.filters.search = searchText;
                concessionairesService.concessionaires.filters.page_size = "all";
                concessionairesService.getConcessionaires().then(function (concessionaires) {
                    deferred.resolve(concessionaires.data);
                });
            }
            return deferred.promise;
        }

        /* Orígenes */
        function getOrigins(searchText, concessionaire) {
            var deferred = $q.defer();
            if (concessionaire) {
                var originsIds = Array.from(new Set(concessionaire.sources.map(function (s) { return s.origin })));
                var origins = originsIds.map(function (origin) {
                    var t = concessionaire.sources.find(function (s) { return s.origin === origin });
                    if (t) {
                        return t.origin_data;
                    }
                });
                var results = searchText ? origins.filter(createFilterFor(searchText)) : origins;
                deferred.resolve(results);
            } else {
                deferred.resolve([]);
            }
            return deferred.promise;
        }

        /* Todos los Orígenes */
        function getAllOrigins(searchText) {
            var deferred = $q.defer();
            originsService.getAllOrigins(searchText).then(function (origins) {
                deferred.resolve(origins);
            });
            return deferred.promise;
        }

        /* Canales */
        function getChannels(searchText, concessionaire, origin) {
            var deferred = $q.defer();
            if (concessionaire && origin) {
                var channelsIds = Array.from(new Set(concessionaire.sources.map(function (s) {
                    return s.channel
                })));
                var channels = channelsIds.map(function (channel) {
                    var t = concessionaire.sources.find(function (s) {
                        return (s.channel === channel && s.origin === origin.id)
                    })
                    if (t) {
                        return t.channel_data;
                    }
                }).filter(function (el) {
                    return el != null;
                });
                var results = searchText ? channels.filter(createFilterFor(searchText)) : channels;
                deferred.resolve(results);
            } else {
                deferred.resolve([]);
            }
            return deferred.promise;
        }

        /* Todos los Canales */
        function getAllChannels(searchText, origin) {
            var deferred = $q.defer();

            if (origin && origin.available_channels_data.length > 0) {
                deferred.resolve(origin.available_channels_data);
            } else {
                deferred.resolve([]);
            }
            return deferred.promise;
        }

        function changeChannel(concessionaire, origin, channel) {
            if (channel) {
                var sourcesIds = Array.from(new Set(concessionaire.sources.map(function (s) { return s.id })));
                var sources = sourcesIds.map(function (source) {
                    return concessionaire.sources.find(function (s) {
                        return (s.id === source && s.origin === origin.id && s.channel === channel.id)
                    });
                }).filter(function (el) {
                    return el != null;
                });

                if (sources.length === 1) {
                    vm.lead.source_data_prov = sources[0];
                }
            }
        }

        function getExposicion() {
            return {
                id: 4,
                name: "Presencial",
                slug: "presencial"
            }
        }

        /* Sources */
        function getSources(searchText, concessionaire, origin, channel) {
            var deferred = $q.defer();
            if (concessionaire && origin && channel) {
                var sourcesIds = Array.from(new Set(concessionaire.sources.map(function (s) { return s.id })));
                var sources = sourcesIds.map(function (source) {
                    return concessionaire.sources.find(function (s) {
                        return (s.id === source && s.origin === origin.id && s.channel === channel.id)
                    });
                }).filter(function (el) {
                    return el != null;
                });
                var results = searchText ? sources.filter(createFilterFor(searchText)) : sources;
                deferred.resolve(results);
            } else {
                deferred.resolve([]);
            }
            return deferred.promise;
        }

        function getFullNamceSource(source) {
            var spaces = " _____ ";
            return gettextCatalog.getString("Origen") + ": " +
                source.origin_data.name + spaces + gettextCatalog.getString("Canal") + ": " +
                source.channel_data.name + " (" + source.data + ")" + spaces + gettextCatalog.getString("Concesionario") + ": " +
                (source.concession_data__name || source.concession_data.name);
        }

        function getFullUserName(user) {
            if (user) {
                return user.first_name + " " + user.last_name;
            }
            return gettextCatalog.getString("Sin asignar");
        }

        /* Clientes */
        function getClients(searchText) {
            var deferred = $q.defer();
            clientsService.getClients(searchText).then(function (clients) {
                deferred.resolve(clients);
            });

            return deferred.promise;
        }

        function getCleanedString(cadena) {
            // Lo queremos devolver limpio en minusculas
            cadena = cadena.toLowerCase();

            // Quitamos acentos y "ñ". Fijate en que va sin comillas el primer parametro
            cadena = cadena.replace(/á/gi, "a");
            cadena = cadena.replace(/é/gi, "e");
            cadena = cadena.replace(/í/gi, "i");
            cadena = cadena.replace(/ó/gi, "o");
            cadena = cadena.replace(/ú/gi, "u");
            return cadena;
        }

        /**
         * Abre el dialogo para crear/editar una lead
         *
         * @param ev
         */
        function openLeadDialog(ev) {
            var deferred = $q.defer();
            var redirect = false;
            vm.saveLead(redirect).then(function (response) {
                if (response.cur_user_can_assign) {

                    usersService.users.filters.userconcession__concessionaire__id = response.concessionaire;
                    usersService.users.filters.is_superuser = false;
                    usersService.users.filters.is_staff = false;
                    usersService.users.filters.is_complex = false;
                    // usersService.users.filters.is_concession_admin='False';
                    $mdDialog.show({
                        controller: 'LeadDialogController',
                        controllerAs: 'vm',
                        templateUrl: 'app/main/leads/dialogs/lead/lead-dialog.html',
                        parent: angular.element($document.body),
                        targetEvent: ev,
                        clickOutsideToClose: true,
                        locals: {
                            Lead: vm.lead,
                            Concessionaire: Concessionaire,
                            Users: usersService.getAllUsers(),
                            event: ev
                        }
                    });
                } else {
                    NotifyService.errorMessage("Usted no puede realizar asignaciones.");
                }
                deferred.resolve();
            }, function () {
                deferred.reject();
            });
            return deferred.promise;
        }

        /**
         * Abre el dialogo para crear/editar el estado de un lead
         *
         * @param ev
         * @param lead
         */
        function openLeadStatusDialog(ev, lead) {

            $mdDialog.show({
                controller: 'LeadStatusDialogController',
                controllerAs: 'vm',
                templateUrl: 'app/main/leads/dialogs/leadStatus/leadStatus-dialog.html',
                parent: angular.element($document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                locals: {
                    Lead: lead,
                    event: ev
                }
            })

        }

        /**
         * Abre el dialogo para crear/editar la fecha del estado de un lead
         *
         * @param ev
         * @param lead
         * @param field
         */
        function openLeadStatusDateDialog(ev, lead, field) {

            $mdDialog.show({
                controller: 'LeadStatusDateDialogController',
                controllerAs: 'vm',
                templateUrl: 'app/main/leads/dialogs/leadStatusDate/leadStatusDate-dialog.html',
                parent: angular.element($document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                locals: {
                    Lead: lead,
                    Field: field,
                    event: ev
                }
            })

        }

        /**
         * Abre el dialogo para crear/editar una lead
         *
         * @param ev
         */
        function openLeadContactDialog(ev) {

            $mdDialog.show({
                controller: 'LeadContactDialogController',
                controllerAs: 'vm',
                templateUrl: 'app/main/leads/dialogs/leadContact/leadContact-dialog.html',
                parent: angular.element($document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                locals: {
                    LeadContacts: vm.lead.contact_history,
                    event: ev
                }
            });

        }

        /**
         * Obtiene la fecha mas lejana de realización
         *
         */
        function getLastRealizationDate(tasks) {
            for (var i in tasks) {
                var date = new Date(0);
                var newDate;
                if (tasks[i].realization_date) {
                    newDate = new Date(tasks[i].realization_date);
                    if (date < newDate) {
                        date = newDate;
                    }
                }
            }
            return date;
        }

        function datediff(first, second) {
            first = new Date(first);
            second = new Date(second);
            // Take the difference between the dates and divide by milliseconds per day.
            // Round to nearest whole number to deal with DST.

            // return Math.round((second-first)/(1000*60*60*24));
            return Math.ceil((second - first) / (1000 * 60 * 60 * 24));
        }

        function eventClientBlur() {
            if (vm.lead.client.phone && vm.lead.client.phone === '+34') {
                vm.lead.client.phone = '';
            }
            if (vm.lead.client.phone && vm.lead.client.phone.length > 8) {
                changeFilter("client__phone__icontains", vm.lead.client.phone);
            }
        }

        function eventClientEmailBlur() {
            if (vm.lead.client.email && vm.lead.client.email.length > 5) {
                changeFilter("client__email__icontains", vm.lead.client.email);
            }
        }

        function setExtension() {
            if (!vm.lead.client.phone || vm.lead.client.phone === '') {
                vm.lead.client.phone = '+34';
            }
        }

        /**
         * Abre el dialogo para indicar si quieres seguir con este lead o ir a otro relacionado
         */
        function openDuplicateLeadsDialog() {
            // Create a new deferred object
            var deferred = $q.defer();

            if (!angular.element(document.body).hasClass('md-dialog-is-showing') && vm.leads.new.filters.id_excluded >= 0) {
                if (((vm.lead.client.phone && vm.lead.client.phone.length > 8) || (vm.lead.client.email && vm.lead.client.email.length > 5)) &&
                    (vm.leads.new.count > 0 || vm.leads.attended.count > 0 || vm.leads.commercial_management.count > 0 || vm.leads.tracing.count > 0 || vm.leads.end.count > 0)) {

                    $mdDialog.show(
                        $mdDialog.alert()
                            .ok(gettextCatalog.getString('OK'))
                            .textContent(
                                gettextCatalog.getString("¡¡Atención existen registros con los mismos datos de contacto revisa sección Coincidentes antes de generar duplicados!!")
                            )
                            .multiple(false)
                    )
                }
            }

            deferred.resolve(true);
            return deferred.promise;
        }

        /**
         * Hace la llamada mediante click2call
         */
        function call(lead) {
            var obj = {
                lead: lead.id
            };

            return click2callsService.saveClick2call(obj).then(function (res) {
                NotifyService.successMessage(gettextCatalog.getString("Acción realizada correctamente"));
                //Si está en gestión y ya tiene alguna llamada preguntamos si desea finalizar el lead
                if (vm.leadsOutgoingCalls.length > 0 && vm.lead.status === 'commercial_management') {
                    finishLeadAfterCall();
                }
                //Si está en seguimiento preguntamos si desea finalizar el lead
                else if (vm.lead.status === 'tracing') {
                    finishLeadAfterCall();
                }

                //Despues de las comprobaciones cambiamos los estados (Importante no cambiar el orden)
                /*if (vm.lead.status === 'commercial_management') {
                    vm.lead.status = 'tracing'
                }
                if (vm.lead.status === 'new') {
                    vm.lead.status = 'commercial_management'
                }*/
            }, function (error) {
                vm.serverErrors = error.data;
                NotifyService.errorMessage(gettextCatalog.getString("Error al realizar la acción.") + " " + (error.data.non_field_errors || ""));
            });
        }

        /**
         * Pregunta si desea finalizar el informe despues de una llamada
         */
        function finishLeadAfterCall() {

            var deferred = $q.defer();
            leadsService.getLead(vm.lead.id).then(function (res) {
                if (res.pending_tasks) {
                    var confirm = $mdDialog.confirm()
                        .title(gettextCatalog.getString('Finalizar lead'))
                        .textContent(gettextCatalog.getString('El sistema ha detectado un seguimiento de este lead ¿Desea finalizar el lead?'))
                        .ariaLabel(gettextCatalog.getString('Finalizar lead'))
                        .clickOutsideToClose(true)
                        .parent(angular.element(document.body))
                        .ok(gettextCatalog.getString('Confirmar'))
                        .cancel(gettextCatalog.getString('Cancelar'));

                    $mdDialog.show(confirm).then(function () {
                        //Abrimos el modal de resultados de gestion
                        openFinishLeadBox();
                    });
                } else {
                    //Abrimos el modal de resultados de gestion
                    openFinishLeadBox();
                }
                deferred.resolve();
            }, function () {
                deferred.reject();
            });
            return deferred.promise;
        }

        /**
         * Abre el dialogo visualizar las historias del lead
         *
         * @param ev
         * @param histories
         */
        function openLeadHistoryDialog(ev, histories) {

            $mdDialog.show({
                controller: 'LeadHistoryDialogController',
                controllerAs: 'vm',
                templateUrl: 'app/main/leads/dialogs/leadHistory/leadHistory-dialog.html',
                parent: angular.element($document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                locals: {
                    LeadHistories: histories,
                    event: ev
                }
            });

        }

        /**
         * Abre el dialogo visualizar las actividades del lead
         *
         * @param ev
         * @param activities
         */
        function openLeadActivityDialog(ev, activities) {

            $mdDialog.show({
                controller: 'LeadActivityDialogController',
                controllerAs: 'vm',
                templateUrl: 'app/main/leads/dialogs/leadActivity/leadActivity-dialog.html',
                parent: angular.element($document.body),
                targetEvent: ev,
                clickOutsideToClose: true,
                locals: {
                    LeadActivities: activities,
                    event: ev
                }
            });

        }

        /**
         * Añade vehiculo
         */
        function addVehicle() {
            vm.lead.vehicles.push({});
        }

        /**
         * Añade vehiculo actular
         */
        function addAppraisal() {
            vm.lead.appraisals.push({
                circulation_date: null,
                buy_date: null,
                registration_date: null,
                last_mechanic_date: null
            });
        }


        /**
         * Borra vehiculo
         */
        function deleteVehicle(i, vehicle) {
            if (vehicle.id) {
                vehiclesService.removeVehicle(vehicle).then(function () {
                    vm.lead.vehicles.splice(i, 1);
                });
            } else {
                vm.lead.vehicles.splice(i, 1);
            }
        }


        /**
         * Borra vehiculo actual
         */
        function deleteAppraisal(i, appraisal) {
            if (appraisal.id) {
                appraisalsService.removeAppraisal(appraisal).then(function () {
                    vm.lead.appraisals.splice(i, 1);
                });
            } else {
                vm.lead.appraisals.splice(i, 1);
            }
        }

        /**
         * Evento que se dispara cuando cambia la fuente
         */
        function changeSource() {
            for (var i in vm.lead.vehicles) {
                vm.lead.vehicles[i].origin = null;
                vm.lead.vehicles[i].media = null;
            }
            if (vm.lead.source_data && vm.lead.source_data.concession) {
                reloadOrigins(vm.lead.source_data.concession);
            }

        }

        /**
         * Evento que se dispara cuando cambia el origen
         */
        function selectOrigin(vehicle) {
            for (var i in vm.origins) {
                if (vm.origins[i].id === vehicle.origin) {
                    vehicle.channelOptions = vm.origins[i].available_channels_data;
                }
            }
        }

        function getNumber(num) {
            return new Array(num);
        }

        /**
         * Abre el dialogo para eliminar una task
         *
         * @param task
         */
        function saveTask(task) {
            if (task.id) {
                var obj = {
                    id: task.id,
                    realization_date: new Date(),
                    realization_date_check: true
                };
                return tasksService.saveTask(obj).then(function (res) {
                    //done
                    reloadLead()
                }, function (error) {
                    NotifyService.errorMessage(gettextCatalog.getString("Error al realizar la solicitud.") + " " + (error.data.non_field_errors || ""));
                });
            } else {
                task.realization_date = new Date();
                task.realization_date_check = true;
            }
        }

        /**
         * Cambiamos el estado y lo reactivamos
         */
        function reactivate(lead) {
            leadsService.reactivateLead(lead.id).then(function (response) {
                reloadLead(response);
                NotifyService.successMessage(gettextCatalog.getString("Lead reactivado correctamente"));
            }, function (error) {
                $rootScope.loadingProgress = false;
                vm.serverErrors = error.data;
                NotifyService.errorMessage(gettextCatalog.getString("Error al reactivar lead.") + " " + (error.data.non_field_errors || ""));
            });
        }


        function sendMail(lead) {
            leadsService.sendMail(lead.id).then(function (response) {

            }, function (error) {
                console.log(error);
            });
        }

        function trustSrc(src) {
            return $sce.trustAsResourceUrl(src);
        }

        function hubspot() {
            return leadsService.hubspot(vm.lead).then(function (response) {
                NotifyService.successMessage(gettextCatalog.getString("Lead sincronizado correctamente"));
            }, function (error) {
                vm.serverErrors = error.data;
                NotifyService.errorMessage(gettextCatalog.getString("Error al sincronizar.") + " " + (error.data.error || ""));
            });
        }

        /**
         * Change filters
         *
         * @param key
         * @param value
         */
        function changeFilter(key, value) {
            vm.filters[key] = value;
            for (var i in vm.leads) {
                vm.leads[i].filters.page = 1;
                vm.leads[i].filters[key] = value;
            }
        }
    }
})();
