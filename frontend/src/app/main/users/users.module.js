(function () {
    'use strict';

    angular
        .module('app.users',
            [

            ]
        )
        .config(config);

    /** @ngInject */
    function config($stateProvider) {

        $stateProvider
            .state('app.users', {
                abstract: true,
                url: '/users',
                resolve:{
                    currentUser: function (AuthService){
                        return AuthService.getCurrentUser().then(function (response) {
                            if (response) {
                                return response;
                            }
                        });
                    }
                }
            })
            .state('app.users.list', {
                url: '/?concessionaire',
                views: {
                    'content@app': {
                        templateUrl: 'app/main/users/views/list/users.html',
                        controller: 'UsersController as vm'
                    }
                },
                resolve: {
                    Concessionaire: function (currentUser, concessionairesService, $stateParams) {
                        if($stateParams.concessionaire) {
                            return concessionairesService.getConcessionaire($stateParams.concessionaire);
                        }
                        return null;
                    },
                    Users: function (currentUser, $rootScope, usersService, Concessionaire) {
                        usersService.users.filters={};
                        usersService.users.filters.online=true;
                        usersService.users.filters.is_active=true;
                        if(Concessionaire) {
                            usersService.users.filters.concessionaire_data = Concessionaire;
                        }
                        return usersService.getUsers();
                    }
                },
                bodyClass: 'users'
            })
            .state('app.users.get', {
                abstract: true,
                url: '/:user/',
                resolve:{
                    User: function (usersService,$stateParams) {
                        return usersService.getUser($stateParams.user);
                    },
                    Schools: function (schoolsService) {
                        schoolsService.schools.filters={};
                        schoolsService.schools.filters.page_size="all";
                        return schoolsService.getSchools();
                    },
                    Courses: function (coursesService) {
                        coursesService.courses.filters={};
                        coursesService.courses.filters.page_size="all";
                        return coursesService.getCourses();
                    },
                    Specialities: function (specialitiesService) {
                        specialitiesService.specialities.filters={};
                        specialitiesService.specialities.filters.page_size="all";
                        return specialitiesService.getSpecialities();
                    },
                }
            })
            .state('app.users.get.detail', {
                url      : 'detail',
                views    : {
                    'content@app': {
                        templateUrl: 'app/main/users/views/detail/user.html',
                        controller : 'UserController as vm'
                    }
                },
                bodyClass: 'todo'
            })
            .state('app.users.get.edit', {
                url      : 'edit',
                views    : {
                    'content@app': {
                        templateUrl: 'app/main/users/views/edit/user.html',
                        controller : 'UserEditController as vm'
                    }
                },
                bodyClass: 'todo'
            });

    }
})();
