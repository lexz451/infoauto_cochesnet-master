(function () {
    'use strict';

    /**
     * Main module of the Fuse
     */
    angular
        .module('fuse', [

            //MomentJS
            'angularMoment',

            'LocalStorageModule',

            'datatables',

            'flow',

            'textAngular',

            // Core
            'app.core',

            // Services
            'app.services',

            // Auntenticación
            // Aquí se establece el baseUrl para la API, por lo que debe ser el primer módulo en cargar despues del core
            'app.auth',
            'app.users',

            // Navigation
            'app.navigation',

            // Toolbar
            'app.toolbar',

            // Dashboard
            'app.dashboard',

            // Metrics
            //'app.metrics',
            'app.campaigns',

            // Informes
            'app.leads',

            // Calendario
            'app.calendar',

            // Tareas
            'app.tasks',

            // Concessionaires
            'app.concessionaires',

            // Origins
            'app.origins',

            // Channels
            'app.channels',

            // Acds
            'app.acds',

            // SFA
            'app.sfas',

            // Imports
            'app.imports',

            // clients
            'app.clients',

            // videos
            'app.videos',

            // geopostcodes
            'app.geopostcodes',

            // Notificaciones
            'app.utils.notify',

            // Filtros
            'app.utils.filters',

            // Directivas
            'app.utils.directives',

            // Servicio para debounce
            'app.utils.debounce',

            'app.utils.factory',

            // Paginacion
            'angularUtils.directives.dirPagination',

            'ngPassword',

            // Traducciones
            'gettext'
        ]);
})();
