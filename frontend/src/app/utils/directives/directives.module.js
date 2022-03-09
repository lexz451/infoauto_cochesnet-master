(function ()
{
    'use strict';

    angular
        .module('app.utils.directives', [])
        .directive('tableAjax', tableAjax)
        .config(config);

    /** @ngInject */
    function config()
    {

    }

    function tableAjax($compile,$timeout) {
        return {
            restrict: 'A',
            scope: {
                tableAjax: '='
            },
            link: function (scope, elem, attrs) {

                var title_table=$(elem).closest(".md-card").find(".md-card-toolbar .md-card-toolbar-heading-text").text();

                if(!window.location.host.includes("localhost")){
                    $.fn.dataTableExt.sErrMode = function(oSettings, iLevel, sMesg){
                        console.log(oSettings, iLevel, sMesg);
                    };
                }

                scope.$watch('tableAjax.data', function (newVal,oldVal) {
                    if(newVal!==oldVal){
                        var numPage=table_tableTools.page();
                        table_tableTools.clear().draw();
                        table_tableTools.rows.add(newVal); // Add new data
                        table_tableTools.columns.adjust().draw(); // Redraw the DataTable
                        if(newVal.length===oldVal.length){
                            table_tableTools.page(numPage).draw( 'page' );
                        }
                        else if(newVal.length>oldVal.length){
                            var data = table_tableTools.rows().data();
                            var id=newVal[newVal.length-1].id;
                            var pos=-1;
                            for(var i in data){
                                if(data[i].id && data[i].id===id){
                                    pos=i;
                                }
                            }
                            if(pos!==-1){
                                var page=pos/table_tableTools.page.len();
                                page=Math.trunc(page);
                                table_tableTools.page(page).draw( 'page' );
                            }
                        }
                    }

                });

                scope.$watch('tableAjax.reload', function (newVal,oldVal) {
                    if(newVal && newVal!==oldVal){
                        table_tableTools.ajax.reload();
                        scope.tableAjax.reload=false;
                    }
                },true);

                function collect() {
                  var ret = {};
                  var len = arguments.length;
                  for (var i=0; i<len; i++) {
                    for (var p in arguments[i]) {
                      if (arguments[i].hasOwnProperty(p)) {
                        ret[p] = arguments[i][p];
                      }
                    }
                  }
                  return ret;
                }

                var $dt_tableTools = $(elem);
                if ($dt_tableTools.length) {

                    var obj=
                        {
                            lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "Todos"]],
                            "language": {
                                "sProcessing": '<div id="page_preloader" class="loaddatatable" style="display: block;opacity:1;width: 200px;height: 200px;margin-top: -100px;margin-left: -100px;top: 50%;left: 50%;border: 1px solid #ccc;"><img src="assets/img/page_preloader.gif" alt=""></div>',
                                "sLengthMenu": "Mostrar"+" _MENU_ "+"registros",
                                "sZeroRecords": "No se encontraron resultados",
                                "sEmptyTable": "Ningún dato disponible en esta tabla",
                                "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
                                "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
                                "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
                                "sInfoPostFix": "",
                                "sSearch": "Buscar"+":",
                                "sUrl": "",
                                "sInfoThousands": ",",
                                "sLoadingRecords": '<div id="page_preloader" class="loaddatatable" style="display: block;opacity:1;width: 200px;height: 200px;margin-top: -100px;margin-left: -100px;top: 50%;left: 50%;border: 1px solid #ccc;"><img src="assets/img/page_preloader.gif" alt=""></div>',
                                "oPaginate": {
                                    "sFirst": "Primero",
                                    "sLast": "Último",
                                    "sNext": "Siguiente",
                                    "sPrevious": "Anterior"
                                },
                                "oAria": {
                                    "sSortAscending": ": "+"Activar para ordenar la columna de manera ascendente",
                                    "sSortDescending": ": "+"Activar para ordenar la columna de manera descendente"
                                }
                            }
                        };

                    obj = collect(obj,scope.tableAjax);
                    var table_tableTools = $dt_tableTools.DataTable(obj);

                    var createButtons=function(){
                        $(".DTTT.uk-text-right").remove();
                        var tt = new $.fn.dataTable.TableTools(table_tableTools, {
                            "sSwfPath": "bower_components/datatables-tabletools/swf/copy_csv_xls_pdf.swf",
                            "aButtons": [
                                {
                                    "sExtends": "copy",
                                    "sButtonClass": "md-raised md-background md-button md-default-theme md-ink-ripple",
                                    "sButtonText": "Copiar"
                                },
                                {
                                    "sExtends": "xls",
                                    "sButtonClass": "md-raised md-background md-button md-default-theme md-ink-ripple",
                                    "sButtonText": "Excel",
                                    "fnCellRender": function ( sValue, iColumn, nTr, iDataIndex ) {
                                        return sValue;
                                    },
                                    "sFileName": "*.xls"
                                },
                                {
                                    "sExtends": "csv",
                                    "sButtonClass": "md-raised md-background md-button md-default-theme md-ink-ripple",
                                    "sButtonText": "CSV",
                                    "fnCellRender": function ( sValue, iColumn, nTr, iDataIndex ) {
                                        return sValue;
                                    }
                                }
                            ]


                        });
                        // $(tt.fnContainer()).insertBefore($dt_tableTools.closest('.content-card').find('.toolbar .options-datatable'));
                        $dt_tableTools.closest('.content-card').find('.toolbar .options-datatable').append($(tt.fnContainer()));
                        $("a.DTTT_button").removeClass("DTTT_button");
                    };
                    $timeout(function(){
                        createButtons();
                    });
                }
            }
        };
    }



})();
