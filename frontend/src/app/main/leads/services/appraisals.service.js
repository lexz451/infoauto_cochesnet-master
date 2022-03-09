(function () {
    'use strict';

    angular
        .module('app.leads')
        .factory('appraisalsService', appraisalsService);

    /** @ngInject */
    function appraisalsService($q, api) {

        var service = {
            removeAppraisal: removeAppraisal
        };

        return service;

        //////////
        
        function removeAppraisal(appraisal){
            var deferred = $q.defer();

            api.appraisals.remove({id: appraisal.id}, appraisalRemoveOK, removeKO);

            // Appraisal borrado correctamente
            function appraisalRemoveOK(response){
                deferred.resolve(response.data);
            }

            // Fallo al borrar appraisal
            function removeKO(response){
                deferred.reject(response);
            }

            return deferred.promise;
        }

    }


})();
