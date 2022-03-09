(function (window, angular, undefined) {
    'use strict';

    angular
        .module('app.utils.directives')
        .directive('formTranslate', formTranslate)
        .directive('formTranslateTemplates', formTranslateTemplates)
        .directive('varTranslate', varTranslate)
        .directive('bindTranslate', bindTranslate)
        .directive('mdAutocompleteTranslate', mdAutocompleteTranslate);

    /** @ngInject */
    function formTranslate($rootScope) {
        return {
            restrict: 'A',
            scope: {
                formTranslate: '='
            },
            compile: function (elem, attrs) {
                /*var $form=$(elem).find("md-dialog-content");

                var html='<md-content><md-tabs md-dynamic-height md-border-bottom>';

                for(var i in $rootScope.languages){
                    var $formClone=$form.clone();

                    //vamos a buscar los campos que sean traducibles solo si no estamos mirando el idioma por defecto
                    if($rootScope.languages[i].code!==$rootScope.languageDefault){
                        var $inputs=$formClone.find("[data-input-translate]");
                        var $errors=$formClone.find("error-messages");

                        $inputs.each(function() {
                            if($(this).attr("name")){
                                $(this).attr("name",$(this).attr("name")+"_"+$rootScope.languages[i].code);
                            }
                            if($(this).attr("data-ng-model")){
                                $(this).attr("data-ng-model",$(this).attr("data-ng-model")+"_"+$rootScope.languages[i].code);
                            }
                        });

                        $errors.each(function() {
                            if($(this).attr("field")){
                                $(this).attr("field",$(this).attr("field")+"_"+$rootScope.languages[i].code);
                            }
                        });

                        // Además añadimos la extension del idioma a los campos adicionales
                        // que luego se usará solo para los campos de tipo texto.
                        var $extraFields=$formClone.find("extra-fields");
                        $extraFields.attr("language","_"+$rootScope.languages[i].code);
                    }

                    html+='<md-tab label="'+$rootScope.languages[i].name+'"><md-content class="md-padding">';

                    html+=$formClone.html();

                    html+='</md-content></md-tab>';

                }

                html+='</md-tabs></md-content>';

               $(elem).find("md-dialog-content").html(html);*/

            }
        };
    }

    /** @ngInject */
    function formTranslateTemplates($rootScope, gettextCatalog) {
        return {
            restrict: 'A',
            scope: {
                formTranslate: '='
            },
            compile: function (elem, attrs) {
                /*var $form=$(elem).find("md-dialog-content");

                var html='<md-content><md-tabs md-dynamic-height md-border-bottom>';

                var languages = [
                    {
                        code:'es',
                        name:gettextCatalog.getString('Español')
                    },
                    {
                        code:'en',
                        name:gettextCatalog.getString('Inglés')
                    },
                    {
                        code:'fr',
                        name:gettextCatalog.getString('Francés')
                    },
                    {
                        code:'pt',
                        name:gettextCatalog.getString('Portugués')
                    },
                    {
                        code:'it',
                        name:gettextCatalog.getString('Italiano')
                    },
                    {
                        code:'de',
                        name:gettextCatalog.getString('Alemán')
                    }
                ];

                for(var i in languages){
                    var $formClone=$form.clone();

                    //vamos a buscar los campos que sean traducibles solo si no estamos mirando el idioma por defecto
                    if(languages[i].code!==$rootScope.languageDefault){
                        var $inputs=$formClone.find("[data-input-translate]");
                        var $keys=$formClone.find(".attachment");

                        $inputs.each(function() {
                            if($(this).attr("name")){
                                $(this).attr("name",$(this).attr("name")+"_"+languages[i].code);
                            }
                            if($(this).attr("data-ng-model")){
                                $(this).attr("data-ng-model",$(this).attr("data-ng-model")+"_"+languages[i].code);
                            }
                            if($(this).attr("required")){
                                $(this).attr("required",false);
                            }
                        });

                        $keys.each(function() {
                            if($(this).attr("data-ng-click")) {
                                $(this).attr("data-ng-click","vm.template.description_"+languages[i].code+"=vm.template.description_"+languages[i].code+"+' {'+key+'} '");
                            }
                        });


                    }

                    html+='<md-tab label="'+languages[i].name+'"><md-content class="md-padding">';

                    html+=$formClone.html();

                    html+='</md-content></md-tab>';

                }

                html+='</md-tabs></md-content>';

               $(elem).find("md-dialog-content").html(html);*/

            }
        };
    }

    /** @ngInject */
    function varTranslate($rootScope) {
        return {
            restrict: 'A',
            compile: function (elem, attrs) {
                /*var text=$(elem).text();
                var arrText=text.split("}}");

                text="";
                for(var i=0; i<arrText.length-1; i++){
                    var t=arrText[i];
                    t=t.replace("{{","");
                    t=t.replace("}}","");
                    text+=" {{"+t.trim()+"_"+$rootScope.languageSelected+" || "+t.trim()+" }}";
                }

                $(elem).text(text);*/

            }
        };
    }
    /** @ngInject */
    function bindTranslate($rootScope) {
        return {
            restrict: 'A',
            compile: function (elem, attrs) {
                /*var text=attrs.ngBindHtml;
                text=text.trim()+"_"+$rootScope.languageSelected+" || "+text;
                attrs.ngBindHtml=text;*/
            }
        };
    }

    /** @ngInject */
    function mdAutocompleteTranslate($rootScope) {
        return {
            restrict: 'A',
            compile: function (elem, attrs) {
                /*
                //Hay que cambiar el atributo mdItemText que es lo que se muestra una vez seleccionado
                // y además hay que traducir las opciones posibles
                var text=attrs.mdItemText;
                // Compruebo que este atributo no sea una función, en el caso de que lo sea debemos controlar
                // la traduccion en la misma función que le pasamos como parámetro.
                // Puedes ver un ejemplo en index.run.js en la función "$rootScope.getFullName()"
                if(text.charAt(text.length-1)!==')'){
                    text=text.trim()+"_"+$rootScope.languageSelected+" || "+text;
                    attrs.mdItemText=text;
                }

                //Una vez cambiado el atributo cambios las opciones
                text=$(elem).find("span[md-highlight-text]").text();

                var arrText=text.split("}}");

                text="";
                for(var i=0; i<arrText.length-1; i++){
                    var t=arrText[i];
                    t=t.replace("{{","");
                    t=t.replace("}}","");
                    text+=" {{"+t.trim()+"_"+$rootScope.languageSelected+" || "+t.trim()+" }}";
                }

                $(elem).find("span[md-highlight-text]").text(text);
                */

            }
        };
    }
})(window, angular);
