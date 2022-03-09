(function () {
    'use strict';

    angular
        .module('app.utils.directives')
        .controller('StarsController', StarsController)
        .directive('stars', starsDirective);
    
    /** @ngInject */
    function StarsController($attrs, $scope, $timeout, gettextCatalog) {
        var vm = this;
    }

    /** @ngInject */
    function starsDirective(api, $q) {
        return {
            restrict: 'E',
            scope: {},
            replace: true,
            bindToController: {
                score: '=score',
            },
            controller: 'StarsController as Stars',
            template: '<div class="tags" layout="row" layout-align="start center" layout-wrap>'+
                                        '<div class="ntag" layout="row" layout-align="start center">'+
                                            '<md-icon ng-if="Stars.score <=0.5" md-font-icon="{{Stars.score >0 ? \'icon-star-half\' : \'icon-star-outline\'}}" class="s16 amber-fg"></md-icon>'+
                                            '<md-icon ng-if="Stars.score >0.5" md-font-icon="{{Stars.score >0 ? \'icon-star\' : \'icon-star-outline\'}}" class="s16 amber-fg"></md-icon>'+
                                            '<md-icon ng-if="Stars.score <=1.5" md-font-icon="{{Stars.score >1 ? \'icon-star-half\' : \'icon-star-outline\'}}" class="s16 amber-fg"></md-icon>'+
                                            '<md-icon ng-if="Stars.score >1.5" md-font-icon="{{Stars.score >1 ? \'icon-star\' : \'icon-star-outline\'}}" class="s16 amber-fg"></md-icon>'+
                                            '<md-icon ng-if="Stars.score <=2.5" md-font-icon="{{Stars.score >2 ? \'icon-star-half\' : \'icon-star-outline\'}}" class="s16 amber-fg"></md-icon>'+
                                            '<md-icon ng-if="Stars.score >2.5" md-font-icon="{{Stars.score >2 ? \'icon-star\' : \'icon-star-outline\'}}" class="s16 amber-fg"></md-icon>'+
                                            '<md-icon ng-if="Stars.score <=3.5" md-font-icon="{{Stars.score >3 ? \'icon-star-half\' : \'icon-star-outline\'}}" class="s16 amber-fg"></md-icon>'+
                                            '<md-icon ng-if="Stars.score >3.5" md-font-icon="{{Stars.score >3 ? \'icon-star\' : \'icon-star-outline\'}}" class="s16 amber-fg"></md-icon>'+
                                        '</div>'+
                                    '</div>',
            link: function (scope, iElement) {

            }
        };
    }
})();
