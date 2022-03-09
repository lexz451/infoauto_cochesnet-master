(function () {
    'use strict';

    angular
        .module('app.services')
        .factory('leadResultsService', leadResultsService);

    /** @ngInject */
    function leadResultsService(gettextCatalog) {

        var service = {

            newLeadResults: [
                {id:'positive', name:gettextCatalog.getString('Ganado')},
                {id:'negative', name:gettextCatalog.getString('Descartado')}
            ],
            resultReasons:{
                positive:[
                    {id:'pedido', name:gettextCatalog.getString('Pedido')},
                    {id:'reservado', name:gettextCatalog.getString('Reservado')}
                ],
                negative:[
                    {id:'publicidad', name:gettextCatalog.getString('Publicidad')},
                    {id:'compra_competencia_precio', name:gettextCatalog.getString('Compra competencia por precio')},
                    {id:'compra_competencia_proximidad', name:gettextCatalog.getString('Compra competencia por proximidad')},
                    {id:'compra_competencia_stock', name:gettextCatalog.getString('Compra competencia por stock')},
                    {id:'no_encaja_producto', name:gettextCatalog.getString('No le encaja el producto')},
                    {id:'no_encaja_precio', name:gettextCatalog.getString('No le encaja el precio')},
                    {id:'no_encaja_cuota', name:gettextCatalog.getString('No le encaja la cuota')},
                    {id:'disconforme_tasacion', name:gettextCatalog.getString('Disconforme con tasación')},
                    {id:'infinanciable', name:gettextCatalog.getString('Infinanciable')},
                    {id:'aplaza_decision', name:gettextCatalog.getString('Aplaza decisión')},
                    {id:'cita_cancelada', name:gettextCatalog.getString('Cita cancelada')},
                    {id:'ilocalizable', name:gettextCatalog.getString('Ilocalizable')},
                    {id:'informacion_cliente_incorrecta', name:gettextCatalog.getString('Información cliente incorrecta')},
                    {id:'duplicado', name:gettextCatalog.getString('Duplicado')},
                    {id:'otro', name:gettextCatalog.getString('Otro')},
                    {id:'caducado', name:gettextCatalog.getString('Caducado')},
                    {id:'vehiculo_ya_vendido', name:gettextCatalog.getString('Vehiculo ya vendido')}
                ]
            },
            leadResults: [
                {
                    id:'positive',
                    name:gettextCatalog.getString('Ganado'),
                    color:"#388E3C"
                },{
                    id:'negative',
                    name:gettextCatalog.getString('Negativo'),
                    color:"rgb(244,67,54)"
                },{
                    id:'reserved_vehicle',
                    name:gettextCatalog.getString('Vehiculo reservado'),
                    color:"#388E3C"
                },{
                    id:'unreachable',
                    name:gettextCatalog.getString('Ilocalizable'),
                    color:"rgb(3,155,229)"
                },{
                    id:'wrong',
                    name:gettextCatalog.getString('Duplicado'),
                    color:"rgb(45,50,62)"
                },{
                    id:'not_available',
                    name:gettextCatalog.getString('No disponible'),
                    color:"rgb(45,50,62)"
                },{
                    id:'error',
                    name:gettextCatalog.getString('Error'),
                    color:"rgb(123,31,162)"
                }
            ],
            leadResultsErrors: [
                {
                    id:'rechaza_financiacion',
                    name:gettextCatalog.getString('Rechaza financiación'),
                    status:'negative'
                },{
                    id:'rechaza_tasacion',
                    name:gettextCatalog.getString('Rechaza tasación'),
                    status:'negative'
                },{
                    id:'rechaza_precio',
                    name:gettextCatalog.getString('Rechaza precio'),
                    status:'negative'
                },{
                    id:'aplaza_compra',
                    name:gettextCatalog.getString('Aplaza compra'),
                    status:'negative'
                },{
                    id:'compra_competencia',
                    name:gettextCatalog.getString('Compra competencia'),
                    status:'negative'
                },{
                    id:'pre-reservado',
                    name:gettextCatalog.getString('Pre-Reservado'),
                    status:'not_available'
                },{
                    id:'reservado-old',
                    name:gettextCatalog.getString('Reservado'),
                    status:'not_available'
                },{
                    id:'publicidad',
                    name:gettextCatalog.getString('Publicidad'),
                    status:'error'
                },{
                    id:'otro_departamento',
                    name:gettextCatalog.getString('Otro Departamento'),
                    status:'error'
                },{
                    id:'error',
                    name:gettextCatalog.getString('Error'),
                    status:'error'
                },
                {
                    id:'compra_competencia_precio',
                    name:gettextCatalog.getString('Compra competencia por precio'),
                    status:'negative'
                },
                {
                    id:'compra_competencia_proximidad',
                    name:gettextCatalog.getString('Compra competencia por proximidad'),
                    status:'negative'
                },
                {
                    id:'compra_competencia_stock',
                    name:gettextCatalog.getString('Compra competencia por stock'),
                    status:'negative'
                },
                {
                    id:'infinanciable',
                    name:gettextCatalog.getString('Infinanciable'),
                    status:'negative'
                },
                {
                    id:'aplaza_decision',
                    name:gettextCatalog.getString('Aplaza decisión'),
                    status:'negative'
                },
                {
                    id:'otro',
                    name:gettextCatalog.getString('Otro'),
                    status:'negative'
                },
                {
                    id:'duplicado',
                    name:gettextCatalog.getString('Duplicado'),
                    status:'negative'
                },
                {
                    id:'cita_cancelada',
                    name:gettextCatalog.getString('Cita cancelada'),
                    status:'negative'
                },
                {
                    id:'informacion_cliente_incorrecta',
                    name:gettextCatalog.getString('Información cliente incorrecta'),
                    status:'negative'
                },
                {
                    id:'ilocalizable',
                    name:gettextCatalog.getString('Ilocalizable'),
                    status:'negative'
                },
                {
                    id:'disconforme_tasacion',
                    name:gettextCatalog.getString('Disconforme con tasación'),
                    status:'negative'
                },
                {
                    id:'caducado',
                    name:gettextCatalog.getString('Caducado'),
                    status:'negative'
                },
                {
                    id:'no_encaja_producto',
                    name:gettextCatalog.getString('No le encaja el producto'),
                    status:'negative'
                },
                {
                    id:'no_encaja_precio',
                    name:gettextCatalog.getString('No le encaja el precio'),
                    status:'negative'
                },
                {
                    id:'no_encaja_cuota',
                    name:gettextCatalog.getString('No le encaja la cuota'),
                    status:'negative'
                },
                {
                    id:'pedido',
                    name:gettextCatalog.getString('Pedido'),
                    status:'positive'
                },
                {
                    id:'reservado',
                    name:gettextCatalog.getString('Reservado'),
                    status:'positive'
                }
            ]
        };

        return service;

    }

})();
