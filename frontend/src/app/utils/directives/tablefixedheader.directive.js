/*
 * Angular Fixed Table Header
 * https://github.com/daniel-nagy/fixed-table-header
 * @license MIT
 * v0.2.1
 */

(function (window, angular, undefined) {
    'use strict';

    angular
        .module('app.utils.directives')
        .directive('tableFixedHeader', tableFixedHeader);

    /** @ngInject */
    function tableFixedHeader($compile, $window) {
        return {
            compile: function (element) {
                var table = {
                    clone: element.find("table").clone(),
                    original: element.find("table")
                };

                var container = element;

                element.css('position', 'relative');
                table.clone.css({
                    position: 'absolute',
                    'z-index':9999
                });


                return function postLink(scope) {
                    table.clone.find("tbody").remove();
                    container.before(table.clone);

                    var header = {
                        clone: table.clone.find("thead"),
                        original: table.original.find("thead")
                    };

                    function cells() {
                        return header.clone.find('th').length;
                    }

                    function getCells(node) {
                        return Array.prototype.map.call(node.find('th'), function (cell) {
                            return angular.element(cell);
                        });
                    }

                    function updateCells() {
                        var cells = {
                            clone: getCells(header.clone),
                            original: getCells(header.original)
                        };


                        cells.clone.forEach(function (clone, index) {
                            if(clone.data('isClone')) {
                                return;
                            }

                            // prevent duplicating watch listeners
                            clone.data('isClone', true);

                            var cell = cells.original[index];
                            var style = $window.getComputedStyle(cell[0]);

                            var setWidth = function () {
                                clone.css({minWidth: style.width, maxWidth: style.width});
                            };

                            var getWidth = function () {
                                return style.width;
                            };

                            var listener = scope.$watch(getWidth, setWidth);

                            $window.addEventListener('resize', setWidth);

                            clone.on('$destroy', function () {
                                listener();
                                $window.removeEventListener('resize', setWidth);
                            });

                            cell.on('$destroy', function () {
                                clone.remove();
                            });
                        });
                    }

                    scope.$watch(cells, updateCells);

                    $compile(table.clone)(scope);
                }
            }
        };
    }
})(window, angular);
