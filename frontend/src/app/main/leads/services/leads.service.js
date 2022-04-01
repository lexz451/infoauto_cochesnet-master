(function () {
    'use strict';

    angular
        .module('app.leads')
        .factory('leadsService', leadsService);

    /** @ngInject */
    function leadsService($q, api, $http) {

        var service = {
            lead: {
                data:{}
            },
            leads: {
                data: [],
                count: 0,
                filters: {}
            },
            leadsNews: {
                data: [],
                count: 0,
                filters: {},
            },
            leadsAttended: {
                data: [],
                count: 0,
                filters: {},
            },
            leadsCommercialManagements: {
                data: [],
                count: 0,
                filters: {},
            },
            leadsTracings: {
                data: [],
                count: 0,
                filters: {},
            },
            leadsEnds: {
                data: [],
                count: 0,
                filters: {},
            },
            leadsIncomingCalls: {
                data: [],
                count: 0,
                filters: {},
            },
            leadsOutgoingCalls: {
                data: [],
                count: 0,
                filters: {},
            },
            leadsHistory: {
                data: [],
                count: 0,
                filters: {},
            },
            leadsActivity: {
                data: [],
                count: 0,
                filters: {},
            },
            getLeads: getLeads,
            getLeadsByUser: getLeadsByUser,
            getAllLeads: getAllLeads,
            getLead: getLead,
            saveLead: saveLead,
            setLeadsByUser: setLeadsByUser,
            changeStatus: changeStatus,
            hubspot: hubspot,
            clone: clone,
            getEmptyLead: getEmptyLead,
            removeLead: removeLead,
            getLeadsNews:getLeadsNews,
            getLeadsAttended:getLeadsAttended,
            getLeadsCommercialManagements:getLeadsCommercialManagements,
            getLeadsTracings:getLeadsTracings,
            getLeadsEnds:getLeadsEnds,
            getLeadsIncomingCalls:getLeadsIncomingCalls,
            getLeadsOutgoingCalls:getLeadsOutgoingCalls,
            getLeadsHistory:getLeadsHistory,
            getLeadsActivity:getLeadsActivity,
            reactivateLead:reactivateLead,
            sendMail:sendMail,
            getDocument:getDocument,
            importLeads:importLeads
        };

        return service;

        //////////

        /**
         * Obtiene el listado de leads
         */
        function getLeads() {
            // Create a new deferred object
            var deferred = $q.defer();
            
            api.leads.get(service.leads.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                service.leads.data = response.results;
                service.leads.count = response.count;

                deferred.resolve(service.leads);
            }

            function getKO(response) {
                //con esto evitamos que den problemas los not found cuando
                // filtramos y estamos en una página que ya no existe
                if(response.status==404 && service.leads.filters.page!=1){
                    service.leads.filters.page=1;
                }
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de leads de un usuario
         */
        function getLeadsByUser(id) {
            // Create a new deferred object
            var deferred = $q.defer();

            service.leads.filters={};
            service.leads.filters.id=id;

            api.leadsByUser.queryAll(service.leads.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                service.leads.data = response;
                service.leads.count = response.length;

                deferred.resolve(service.leads);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de leads filtrando unicamente por el texto dado y sin guardar en el servicio
         *
         * @param search
         */
        function getAllLeads(search) {
            // Create a new deferred object
            var deferred = $q.defer();
            var f=angular.copy(service.leads.filters);
            f.search=search;
            f.page_size="all";
            api.leads.get(f, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                deferred.resolve(response.results);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene los datos de una lead determinado por su ID
         *
         * @param id
         */
        function getLead(id) {
            // Create a new deferred object
            var deferred = $q.defer();
            api.leads.get({id: id}, getOK, getKO);
            return deferred.promise;

            function getOK(response) {
                service.lead.data = response;
                deferred.resolve(response);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Guarda la lead que se pasa como parámetro. Si ya existe actualiza el existente.
         *
         * @param form
         */
        function saveLead(form) {
            var deferred = $q.defer();

            var lead=angular.copy(form);

            if(lead.client && lead.client.province_data && lead.client.province_data.id){
                lead.client.province=lead.client.province_data.id;
            }
            if(lead.client && lead.client.location_data && lead.client.location_data.id){
                lead.client.location=lead.client.location_data.id;
            }

            if(lead.source_data_prov && lead.source_data_prov.id){
                lead.source=lead.source_data_prov.id;
            }

            if(lead.concessionaire_data && lead.concessionaire_data.id){
                lead.concessionaire=lead.concessionaire_data.id;
            }

            if(lead.user_data && lead.user_data.id){
                lead.user=lead.user_data.id;
            }

            if(lead.client && lead.client.business_activity_data && lead.client.business_activity_data.id){
                lead.client.business_activity=lead.client.business_activity_data.id;
            }

            if(lead.client && lead.client.sector_data && lead.client.sector_data.id){
                lead.client.sector=lead.client.sector_data.id;
            }

            for (var i in lead.vehicles) {
                //brand
                if(lead.vehicles[i].brand_model_data && lead.vehicles[i].brand_model_data.name){
                    lead.vehicles[i].brand_model=lead.vehicles[i].brand_model_data.name;
                }
                if(lead.vehicles[i].brand_model_data && lead.vehicles[i].brand_model_data.id){
                    lead.vehicles[i].brand_model+="___"+lead.vehicles[i].brand_model_data.id;
                }

                //model
                if(lead.vehicles[i].model_data && lead.vehicles[i].model_data.model_name){
                    lead.vehicles[i].model=lead.vehicles[i].model_data.model_name;
                }
                if(lead.vehicles[i].model_data && lead.vehicles[i].model_data.id){
                    lead.vehicles[i].model+="___"+lead.vehicles[i].model_data.id;
                }

                //version
                if(lead.vehicles[i].version_data && lead.vehicles[i].version_data.version_name){
                    lead.vehicles[i].version=lead.vehicles[i].version_data.version_name;
                }
                if(lead.vehicles[i].version_data && lead.vehicles[i].version_data.id){
                    lead.vehicles[i].version+="___"+lead.vehicles[i].version_data.id;
                }
		if (lead.vehicles[i].rejection_reason == "") {
                    lead.vehicles[i].rejection_reason = null;
                }
		if (lead.vehicles[i].segment == "") {
                    lead.vehicles[i].segment = "other";
                }
		if (!lead.vehicles[i].purchase_method) {
		    lead.vehicles[i].purchase_method = "count";	
		}
		if (!lead.vehicles[i].purchase_description) {
                    lead.vehicles[i].purchase_description = "";
                }
            }

            for (var i in lead.appraisals) {
                //brand
                if(lead.appraisals[i].brand_data && lead.appraisals[i].brand_data.name){
                    lead.appraisals[i].brand=lead.appraisals[i].brand_data.name;
                }
                if(lead.appraisals[i].brand_data && lead.appraisals[i].brand_data.id){
                    lead.appraisals[i].brand+="___"+lead.appraisals[i].brand_data.id;
                }

                //model
                if(lead.appraisals[i].model_data && lead.appraisals[i].model_data.model_name){
                    lead.appraisals[i].model=lead.appraisals[i].model_data.model_name;
                }
                if(lead.appraisals[i].model_data && lead.appraisals[i].model_data.id){
                    lead.appraisals[i].model+="___"+lead.appraisals[i].model_data.id;
                }

                //version
                if(lead.appraisals[i].version_data && lead.appraisals[i].version_data.version_name){
                    lead.appraisals[i].version=lead.appraisals[i].version_data.version_name;
                }
                if(lead.appraisals[i].version_data && lead.appraisals[i].version_data.id){
                    lead.appraisals[i].version+="___"+lead.appraisals[i].version_data.id;
                }

            }

            if (form.id) {
                api.leads.update(lead, updateOK, saveKO);
            } else {
                api.leads.create(lead, createOK, saveKO);
            }

            return deferred.promise;


            function createOK(response) {
                // Store the leads
                service.leads.data.push(response);
                service.leads.count ++;
                deferred.resolve(response);
            }

            function updateOK(response) {
                // Actauliza el listado
                for (var i = 0; i < service.leads.data.length; i++) {
                    if (service.leads.data[i].id === response.id) {
                        service.leads.data[i] = angular.copy(response);
                    }
                }
                deferred.resolve(response);
            }

            function saveKO(response) {
                deferred.reject(response);
            }

        }

        /**
         * Guarda la lead que se pasa como parámetro. Si ya existe actualiza el existente.
         *
         * @param form
         */
        function setLeadsByUser(form) {
            var deferred = $q.defer();

            api.setLeadsByUser.create(form, createOK, saveKO);


            return deferred.promise;


            function createOK(response) {
                deferred.resolve(response);
            }

            function saveKO(response) {
                deferred.reject(response);
            }

        }

        /**
         * Guarda la lead que se pasa como parámetro. Si ya existe actualiza el existente.
         *
         * @param form
         */
        function changeStatus(form) {
            var deferred = $q.defer();

            var lead=angular.copy(form);

            api.leads.leadsStatus(lead, updateOK, saveKO);

            return deferred.promise;

            function updateOK(response) {
                // Actauliza el listado
                for (var i = 0; i < service.leads.data.length; i++) {
                    if (service.leads.data[i].id === response.id) {
                        service.leads.data[i] = angular.copy(response);
                    }
                }
                deferred.resolve(response);
            }

            function saveKO(response) {
                deferred.reject(response);
            }

        }

        /**
         * Guarda la lead que se pasa como parámetro. Si ya existe actualiza el existente.
         *
         * @param form
         */
        function hubspot(form) {
            var deferred = $q.defer();

            var lead= {
                id: form.id,
            }

            api.leads.leadsHubspot(lead, updateOK, saveKO);

            return deferred.promise;

            function updateOK(response) {
                deferred.resolve(response);
            }

            function saveKO(response) {
                deferred.reject(response);
            }

        }

        /**
         * Clona un lead
         *
         * @param lead
         */
        function clone(lead) {
            var deferred = $q.defer();

            api.leads.clone({id: lead.id}, createOK, saveKO);

            return deferred.promise;


            function createOK(response) {
                // Store the leads
                service.leads.data.push(response);
                service.leads.count ++;
                deferred.resolve(response);
            }

            function saveKO(response) {
                deferred.reject(response);
            }

        }

        /**
         * Devuelve un lead vacío
         */
        function getEmptyLead() {
            return {
                client:{},
                vehicles:[{}],
                appraisals:[{
                    circulation_date:null,
                    buy_date:null,
                    registration_date:null,
                    last_mechanic_date:null
                }],
                note:[],
                tags:[],
                request:{
                    task:[]
                },
                // score:null
            };
        }
        
        function removeLead(lead){
            var deferred = $q.defer();

            api.leads.remove({id: lead.id}, leadRemoveOK, removeKO);

            // Lead borrado correctamente
            function leadRemoveOK(response){
                // Quitamos la lead en los datos locales
                for (var i = 0; i < service.leads.data.length; i++) {
                    if (service.leads.data[i].id === lead.id) {
                        service.leads.data.splice(i,1);
                        service.leads.count -= 1;
                        break;
                    }
                }
                deferred.resolve(response.data);
            }

            // Fallo al borrar lead
            function removeKO(response){
                deferred.reject(response);
            }

            return deferred.promise;
        }

        ////// PARA EL BOARD /////
        /**
         * Obtiene el listado de leadsNews
         */
        function getLeadsNews() {
            // Create a new deferred object
            var deferred = $q.defer();

            api.leadsNews.get(service.leadsNews.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                if(service.leadsNews.filters.page>1){
                   service.leadsNews.data=service.leadsNews.data.concat(response.results);
                }else{
                    service.leadsNews.data = response.results;
                }

                service.leadsNews.count = response.count;
                deferred.resolve(service.leadsNews);
            }

            function getKO(response) {
                //con esto evitamos que den problemas los not found cuando
                // filtramos y estamos en una página que ya no existe
                if(response.status==404 && service.leadsNews.filters.page!=1){
                    service.leadsNews.filters.page=1;
                }
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de leadsAttended
         */
        function getLeadsAttended() {
            // Create a new deferred object
            var deferred = $q.defer();

            api.leadsAttended.get(service.leadsAttended.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                if(service.leadsAttended.filters.page>1){
                   service.leadsAttended.data=service.leadsAttended.data.concat(response.results);
                }else{
                    service.leadsAttended.data = response.results;
                }

                service.leadsAttended.count = response.count;
                deferred.resolve(service.leadsAttended);
            }

            function getKO(response) {
                //con esto evitamos que den problemas los not found cuando
                // filtramos y estamos en una página que ya no existe
                if(response.status==404 && service.leadsAttended.filters.page!=1){
                    service.leadsAttended.filters.page=1;
                }
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de leadsCommercialManagements
         */
        function getLeadsCommercialManagements() {
            // Create a leadsCommercialManagement deferred object
            var deferred = $q.defer();

            api.leadsCommercialManagements.get(service.leadsCommercialManagements.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                if(service.leadsCommercialManagements.filters.page>1){
                   service.leadsCommercialManagements.data=service.leadsCommercialManagements.data.concat(response.results);
                }else{
                    service.leadsCommercialManagements.data = response.results;
                }

                service.leadsCommercialManagements.count = response.count;
                deferred.resolve(service.leadsCommercialManagements);
            }

            function getKO(response) {
                //con esto evitamos que den problemas los not found cuando
                // filtramos y estamos en una página que ya no existe
                if(response.status==404 && service.leadsCommercialManagements.filters.page!=1){
                    service.leadsCommercialManagements.filters.page=1;
                }
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de leadsTracings
         */
        function getLeadsTracings() {
            // Create a tracing deferred object
            var deferred = $q.defer();

            api.leadsTracings.get(service.leadsTracings.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                if(service.leadsTracings.filters.page>1){
                   service.leadsTracings.data=service.leadsTracings.data.concat(response.results);
                }else{
                    service.leadsTracings.data = response.results;
                }

                service.leadsTracings.count = response.count;
                deferred.resolve(service.leadsTracings);
            }

            function getKO(response) {
                //con esto evitamos que den problemas los not found cuando
                // filtramos y estamos en una página que ya no existe
                if(response.status==404 && service.leadsTracings.filters.page!=1){
                    service.leadsTracings.filters.page=1;
                }
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de leadsEnds
         */
        function getLeadsEnds() {
            // Create a end deferred object
            var deferred = $q.defer();

            api.leadsEnds.get(service.leadsEnds.filters, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                if(service.leadsEnds.filters.page>1){
                   service.leadsEnds.data=service.leadsEnds.data.concat(response.results);
                }else{
                    service.leadsEnds.data = response.results;
                }

                service.leadsEnds.count = response.count;
                deferred.resolve(service.leadsEnds);
            }

            function getKO(response) {
                //con esto evitamos que den problemas los not found cuando
                // filtramos y estamos en una página que ya no existe
                if(response.status==404 && service.leadsEnds.filters.page!=1){
                    service.leadsEnds.filters.page=1;
                }
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de leadsIncomingCalls
         */
        function getLeadsIncomingCalls(id) {
            // Create a end deferred object
            var deferred = $q.defer();

            var f=angular.copy(service.leadsIncomingCalls.filters);
            f.page_size="all";
            f.id=id;

            api.leadsIncomingCalls.get(f, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                service.leadsIncomingCalls.data = response.results;
                service.leadsIncomingCalls.count = response.count;

                deferred.resolve(service.leadsIncomingCalls);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de leadsOutgoingCalls
         */
        function getLeadsOutgoingCalls(id) {
            // Create a end deferred object
            var deferred = $q.defer();

            var f=angular.copy(service.leadsOutgoingCalls.filters);
            f.page_size="all";
            f.id=id;

            api.leadsOutgoingCalls.get(f, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                service.leadsOutgoingCalls.data = response.results;
                service.leadsOutgoingCalls.count = response.count;

                deferred.resolve(service.leadsOutgoingCalls);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de leadsHistory
         */
        function getLeadsHistory(id) {
            // Create a end deferred object
            var deferred = $q.defer();

            var f=angular.copy(service.leadsHistory.filters);
            f.page_size="all";
            f.id=id;

            api.leadsHistory.get(f, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                service.leadsHistory.data = response.results;
                service.leadsHistory.count = response.count;

                deferred.resolve(service.leadsHistory);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Obtiene el listado de leadsActivity
         */
        function getLeadsActivity(id) {
            // Create a end deferred object
            var deferred = $q.defer();

            var f=angular.copy(service.leadsActivity.filters);
            f.page_size="all";
            f.lead=id;

            api.leadActions.get(f, getOK, getKO);

            return deferred.promise;

            function getOK(response) {
                service.leadsActivity.data = response.results;
                service.leadsActivity.count = response.count;

                deferred.resolve(service.leadsActivity);
            }

            function getKO(response) {
                deferred.reject(response);
            }
        }


        /**
         * Cambiamos el lead y lo reactivamos
         */
        function reactivateLead(id) {
            var deferred = $q.defer();

            // var lead = angular.copy(form);
             var f= {};

            f.id=id;
            api.leadsReactivate.create(f, createOK, saveKO);

            return deferred.promise;

            function createOK(response) {
                deferred.resolve(response);
            }

            function saveKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Marcamos que vamos a mandar mail
         */
        function sendMail(id) {
            var deferred = $q.defer();

            // var lead = angular.copy(form);
             var f= {};

            f.id=id;
            api.leadsMail.create(f, createOK, saveKO);

            return deferred.promise;

            function createOK(response) {
                deferred.resolve(response);
            }

            function saveKO(response) {
                deferred.reject(response);
            }
        }

        /**
         * Descarga un documento excel con leads de ejemplo
         *
         */
        function getDocument() {
            var deferred = $q.defer();

            $http.get(api.baseUrl + 'lead_importer/download_template/', {responseType:'arraybuffer',timeout:60*60*1000}).then(getOK, getKO);

            return deferred.promise;

            function getOK(response){
                deferred.resolve(response.data);
            }

            function getKO(response){
                deferred.reject(response);
            }
        }

        /**
         * Importa los leads de un archivo excel
         *
         */
        function importLeads() {
            var deferred = $q.defer();

            // Preparamos la filen para la subida al servidor
            // Comprobamos si existe en file.element y de forma directa ya
            // que parece que en ios no lo encuentra bien con el file.element.
            var file_data = null;
            var $fileUploader = $("#file-uploader");
            var files = $fileUploader.prop('files');

            if (files && files.length) {
                file_data = files[0];
            }

            //Convertimos los datos aun FormData para poder enviar el archivo
            var formData = new FormData();

            if (file_data){
                formData.append('file', file_data);
            }

            $http.post(api.baseUrl + 'lead_importer/upload/', formData, { transformRequest: angular.identity,
                headers: {'Content-Type': undefined}, responseType:'arraybuffer',timeout:60*60*1000}).then(createOK, saveKO);

            return deferred.promise;

            function createOK(response) {
                deferred.resolve(response.data);
            }

            function saveKO(response) {
                deferred.reject(response);
            }

        }

    }


})();
