(function () {
    'use strict';

    angular
        .module('app.users')
        .controller('LeadByUserDialogController', LeadByUserDialogController);

    /** @ngInject */
    function LeadByUserDialogController($mdDialog, leadsService, User, NotifyService, usersService, $q, gettextCatalog) {
        var vm = this;

        // Data
        vm.title=gettextCatalog.getString("Reasignación de leads")
        vm.leads=leadsService.leads;
        vm.user=User;
        vm.concessionaires={};

        init();

        // Methods
        vm.toggleActive = toggleActive;
        vm.getUsers = getUsers;
        vm.getFullUserName = getFullUserName;
        vm.reasign = reasign;
        vm.isFormDisabled = isFormDisabled;
        vm.closeDialog = closeDialog;

        //////////
        function init(){
            var c={};
            for(var i in vm.leads.data){
                if(!c['c'+vm.leads.data[i].concession_id] && vm.leads.data[i].concession_id){
                    c['c'+vm.leads.data[i].concession_id]={
                        id:vm.leads.data[i].concession_id,
                        name:vm.leads.data[i].concession_name,
                        leads:[],
                        user_data:null
                    }
                }
                if(vm.leads.data[i].concession_id){
                    c['c'+vm.leads.data[i].concession_id].leads.push(vm.leads.data[i]);
                }
            }
            vm.concessionaires=c;
        }

        /* toggle */
        function toggleActive(user) {
            //realizamos la baja/alta
            var obj={
                id:user.id,
                is_active:!user.is_active
            };
            return usersService.saveUser(obj).then(function(res){
                if(res.is_active){
                    NotifyService.successMessage(gettextCatalog.getString("Usuario dado de alta correctamente"));
                }else{
                    NotifyService.successMessage(gettextCatalog.getString("Usuario dado de baja correctamente"));
                }
                closeDialog();
            }, function(error){
                vm.serverErrors = error.data;
                if(obj.is_active){
                    NotifyService.errorMessage(gettextCatalog.getString("Error al dar de alta a este usuario.") +" "+ (error.data.non_field_errors || ""));
                }else{
                    NotifyService.errorMessage(gettextCatalog.getString("Error al dar de baja a este usuario.") +" "+ (error.data.non_field_errors || ""));
                }
            });

        }

        /* Usuarios */
        function getUsers(searchText, Concessionaire) {
            var deferred = $q.defer();
            usersService.getAllUsersConcessionaire(searchText,Concessionaire).then(function(users){
                deferred.resolve(users);
            });

            return deferred.promise;
        }

        function getFullUserName(user) {
            return user.first_name+" "+user.last_name;
        }

        function reasign(concessionaire) {
            var obj={
                id:concessionaire.user_data.id,
                leads:[]
            };
            for(var i in concessionaire.leads){
                obj.leads.push(concessionaire.leads[i].id);
            }
            return leadsService.setLeadsByUser(obj).then(function (res) {
                delete vm.concessionaires['c'+concessionaire.id];
                NotifyService.successMessage(gettextCatalog.getString("Leads reasignados correctamente"));
            },function (error) {
                NotifyService.errorMessage(gettextCatalog.getString("Error al reasignar leads.") +" "+ (error.data.non_field_errors || ""));
            })
        }

        function isFormDisabled(){
            for(var i in vm.concessionaires){
                if(vm.concessionaires[i].leads.length>0){
                    return true;
                }
            }
            return false;
        }
        
        /**
         * Cerrar el cuadro de diálogo sin cambios
         */
        function closeDialog() {
            $mdDialog.hide();
        }

    }
})();
