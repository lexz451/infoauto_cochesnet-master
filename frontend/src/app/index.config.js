(function () {
  'use strict';

  angular
    .module('fuse')
    .config(config);

  /** @ngInject */
  function config($httpProvider, $resourceProvider, $mdThemingProvider, $provide, $mdDateLocaleProvider, moment,
                  paginationTemplateProvider, localStorageServiceProvider, flowFactoryProvider, NotifyServiceProvider) {

    // Configura el CSRF_TOKEN
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';

    localStorageServiceProvider.setPrefix('config');

    // Don't strip trailing slashes from calculated URLs
    $resourceProvider.defaults.stripTrailingSlashes = false;

    $mdThemingProvider.theme('toast-error');
    $mdThemingProvider.theme('toast-success');

    // Configuración del datepicker en español
    $mdDateLocaleProvider.months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
      'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
    $mdDateLocaleProvider.shortMonths = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
      'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
    $mdDateLocaleProvider.days = ['Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sábado'];
    $mdDateLocaleProvider.shortDays = ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sá'];
    // Can change week display to start on Monday.
    $mdDateLocaleProvider.firstDayOfWeek = 1;
    // Optional.
    //$mdDateLocaleProvider.dates = [1, 2, 3, 4, 5, 6, 7,8,9,10,11,12,13,14,15,16,17,18,19,
    //                               20,21,22,23,24,25,26,27,28,29,30,31];
    // In addition to date display, date components also need localized messages
    // for aria-labels for screen-reader users.
    $mdDateLocaleProvider.weekNumberFormatter = function (weekNumber) {
      return 'Semana ' + weekNumber;
    };
    $mdDateLocaleProvider.msgCalendar = 'Calendario';
    $mdDateLocaleProvider.msgOpenCalendar = 'Abrir calendario';

    $mdDateLocaleProvider.parseDate = function (dateString) {
      var m = moment(dateString, 'D/M/YYYY', true);
      return m.isValid() ? m.toDate() : new Date(NaN);
    };

    $mdDateLocaleProvider.formatDate = function (date) {
      var m = moment(date);
      return m.isValid() ? m.format('D/M/YYYY') : '';
    };

    paginationTemplateProvider.setPath('app/utils/templates/dirPagination.tpl.html');



    // Modifica la directiva md-button para permitir hacer un debouce
    // automático del click
    $provide.decorator('mdButtonDirective', function ($delegate) {
      var directive = $delegate[0];
      var oldTemplate = directive.template;   // Guarda el antiguo template
      var i = 0;                              // Contador para nombrar de forma automática la variable del estado de la promesa
      var varName = "__promiseStatusVar";     // Nombre de la variable que contiene el estado de la promesa

      directive.template = getTemplate;       // Asigna el nuevo template

      function getTemplate(element, attr) {
        if (angular.isUndefined(attr.debouceClick)) {
          return oldTemplate(element, attr);
        }

        // El atributo debouce-click permite definir el nombre de la variable que se usará para
        // guardar el estado de la promesa
        if (attr.debouceClick !== "") {
          varName = attr.debouceClick;
        }

        // Aumentamos el contador en cada instancia de la directiva
        i++;

        // Modifica el atributo ng-click para guardar el estado de la promesa
        attr.ngClick = varName + i + ' = (' + attr.ngClick + ' | promiseStatus)';

        // Modifica el atributo ng-disabled para incluir el estado de la promesa
        var ngDisabledString = "";
        if (attr.ngDisabled === undefined) {
          ngDisabledString = 'ng-disabled="' + varName + i + '.inProgress"';
        } else {
          attr.ngDisabled = "(" + attr.ngDisabled + ") || (" + varName + i + ".inProgress )";
        }

        // Modificaciones del template
        var btnType = (typeof attr.type === 'undefined') ? 'button' : attr.type;
        var layout = (typeof attr.layout === 'undefined') ? 'row' : attr.layout;
        var layoutAlign = (typeof attr.layoutAlign === 'undefined') ? 'center center' : attr.layoutAlign;
        return '<button ' + ngDisabledString + ' class="md-button" type="' + btnType + '"><ng-transclude layout="' + layout + '" layout-align="' + layoutAlign + '"></ng-transclude><md-progress-circular ng-show="' + varName + i + '.inProgress" class="for-button" md-diameter="16" md-mode="indeterminate"></md-progress-circular> </button>';
      }

      return $delegate;
    });

    // Modifica la directiva input para eliminar os errores de servidor cuando el usuario modifica el contenido
    $provide.decorator('inputDirective', function ($delegate) {
      var directive = $delegate[0];

      // Override del link
      directive.compile = function () {
        return function (scope, element, attrs, ctrl) {
          directive.link.pre.apply(this, arguments);
          element.on('change', function () {
            if (ctrl[0]) {
              scope.$apply(function () {
                ctrl[0].$setValidity('serverError', true);
              });
            }
          });
          element.on('focus', function () {
            if (ctrl[0]) {
              ctrl[0].$setValidity('serverError', true);
            }
          });
          element.on('keydown', function () {
            if (ctrl[1]) {
              scope.$apply(function () {
                ctrl[1].$setValidity('serverError', true);
              });
            }
          });

        };
      };

      return $delegate;
    });

    // Modifica la directiva input para eliminar os errores de servidor cuando el usuario modifica el contenido
    $provide.decorator('textareaDirective', function ($delegate) {
      var directive = $delegate[0];

      // Override del link
      directive.compile = function () {
        return function (scope, element, attrs, ctrl) {
          directive.link.pre.apply(this, arguments);
          element.on('change', function () {
            if (ctrl[0]) {
              scope.$apply(function () {
                ctrl[0].$setValidity('serverError', true);
              });
            }
          });
          element.on('focus', function () {
            if (ctrl[0]) {
              ctrl[0].$setValidity('serverError', true);
            }
          });
          element.on('keydown', function () {
            if (ctrl[1]) {
              scope.$apply(function () {
                ctrl[1].$setValidity('serverError', true);
              });
            }
          });

        };
      };

      return $delegate;
    });

    // Modifica la directiva select para eliminar os errores de servidor cuando el usuario modifica el contenido
    $provide.decorator('selectDirective', function ($delegate) {
      var directive = $delegate[0];

      // Override del link
      directive.compile = function () {
        return function (scope, element, attrs, ctrl) {
          var $directiveElement=element.parent().find("md-select");
          var form=element.closest("form").attr("name");
          var name=$directiveElement.attr("name");
          directive.link.pre.apply(this, arguments);
          $directiveElement.on('focus', function () {
            if (scope[form] && scope[form][name]) {
                scope[form][name].$setValidity('serverError', true);
            }
          });

        };
      };

      return $delegate;
    });

    // Text Angular options
    $provide.decorator('taOptions', [
      '$delegate', function (taOptions) {
        taOptions.toolbar = [
          ['bold', 'italics', 'underline', 'ul', 'ol', 'quote']
        ];

        taOptions.classes = {
          focussed: 'focussed',
          toolbar: 'ta-toolbar',
          toolbarGroup: 'ta-group',
          toolbarButton: 'md-button',
          toolbarButtonActive: 'active',
          disabled: '',
          textEditor: 'form-control',
          htmlEditor: 'form-control'
        };

        return taOptions;
      }
    ]);

    // Text Angular tools
    $provide.decorator('taTools', [
      '$delegate', function (taTools) {
        taTools.quote.iconclass = 'icon-format-quote';
        taTools.bold.iconclass = 'icon-format-bold';
        taTools.italics.iconclass = 'icon-format-italic';
        taTools.underline.iconclass = 'icon-format-underline';
        taTools.strikeThrough.iconclass = 'icon-format-strikethrough';
        taTools.ul.iconclass = 'icon-format-list-bulleted';
        taTools.ol.iconclass = 'icon-format-list-numbers';
        taTools.redo.iconclass = 'icon-redo';
        taTools.undo.iconclass = 'icon-undo';
        taTools.clear.iconclass = 'icon-close-circle-outline';
        taTools.justifyLeft.iconclass = 'icon-format-align-left';
        taTools.justifyCenter.iconclass = 'icon-format-align-center';
        taTools.justifyRight.iconclass = 'icon-format-align-right';
        taTools.justifyFull.iconclass = 'icon-format-align-justify';
        taTools.indent.iconclass = 'icon-format-indent-increase';
        taTools.outdent.iconclass = 'icon-format-indent-decrease';
        taTools.html.iconclass = 'icon-code-tags';
        taTools.insertImage.iconclass = 'icon-file-image-box';
        taTools.insertLink.iconclass = 'icon-link';
        taTools.insertVideo.iconclass = 'icon-filmstrip';

        return taTools;
      }
    ]);

    // Modifica la directiva radio-group para eliminar os errores de servidor cuando el usuario modifica el valor
    $provide.decorator('mdRadioGroupDirective', function ($delegate) {
      var directive = $delegate[0];

      // Override del link
      directive.compile = function () {
        return function (scope, element, attrs, ctrl) {
          directive.link.pre.apply(this, arguments);
          element.on('mousedown', function () {
            if (ctrl[1]) {
              scope.$apply(function () {
                ctrl[1].$setValidity('serverError', true);
              });
            }
          });
          element.on('keydown', function () {
            if (ctrl[1]) {
              scope.$apply(function () {
                ctrl[1].$setValidity('serverError', true);
              });
            }
          });

        };
      };

      return $delegate;

    });

    function utf8Encode(unicodeString) {
        if (typeof unicodeString != 'string') throw new TypeError('parameter ‘unicodeString’ is not a string');
        const utf8String = unicodeString.replace(
            /[\u0080-\u07ff]/g,  // U+0080 - U+07FF => 2 bytes 110yyyyy, 10zzzzzz
            function(c) {
                var cc = c.charCodeAt(0);
                return String.fromCharCode(0xc0 | cc>>6, 0x80 | cc&0x3f); }
        ).replace(
            /[\u0800-\uffff]/g,  // U+0800 - U+FFFF => 3 bytes 1110xxxx, 10yyyyyy, 10zzzzzz
            function(c) {
                var cc = c.charCodeAt(0);
                return String.fromCharCode(0xe0 | cc>>12, 0x80 | cc>>6&0x3F, 0x80 | cc&0x3f); }
        );
        return utf8String;
    }

    flowFactoryProvider.defaults = {
        target: "/api/documents/",
        headers: function (file, chunk, isTest) {
            return {
                'Authorization': 'Token ' + ((localStorage['config.token']) ? localStorage['config.token'].split('"')[1] : '')
            };
        },
        testChunks: false,
        chunkSize: 1024*1024*1024*1024*1024,
        fileParameterName: "document",
        query:function(file){
            return {name:utf8Encode(file.name)};
        }
    };

    flowFactoryProvider.on('catchAll', function (event,e) {
      if(event==="error"){
        var error = JSON.parse(e);
        NotifyServiceProvider.$get().errorMessage(error.detail);

      }
    });

  }

})();
