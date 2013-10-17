var module = angular.module('commonDirs', []);

// TODO Stop using this when the following issue is fixed:
// https://github.com/angular/angular.js/issues/1460
module.directive('autoFillSync', ['$timeout', 
                                  function($timeout) 
{
  return {
    require: 'ngModel',
    link: function(scope, elem, attrs, ngModel) {
      var origVal = elem.val();
      $timeout(function () {
        var newVal = elem.val();
        if(ngModel.$pristine && origVal !== newVal) {
          ngModel.$setViewValue(newVal);
        }
      }, 500);
    }
  }
}]);

module.directive('explorerLink', function() {
  return {
    scope: {
      address: "@explorerLink"
    },
    template: '<a href="{{explorer}}/{{type}}/{{address}}">{{address}}</a>',
    link: function  (scope, element, attrs)
    {
      scope.type = attrs.type || 'address';
      var currency = attrs.currency || 'frc';

      if (currency == 'frc') {
        scope.explorer = 'http://cryptocoinexplorer.com:4750'
      } else if (currency == 'btc') {
        scope.explorer = 'http://blockexplorer.com';
      }
    }
  }
});

module.directive('panelTittle', function($parse) {

  return {
    transclude: true,
    replace: true,
    scope:{
      width: "@",
      bootstrapClass: "=bootstrapClass",
      tittleLabel: "@panelTittle"
    },
    template: 
    '<div class="col-sm-{{width || 9}}">' +
      '<div class="panel panel-{{bootstrapClass || \'default\'}}">' +
      '<div class="panel-heading">' +
      '  <h3 class="panel-title">{{tittleLabel}}</h3>' + 
      '</div>' +
      '<div class="panel-body" ng-transclude></div>' +
      '</div>' +
      '</div>',
  }
});

module.directive('formInputId', function() {
  return {
    transclude: true,
    priority: 1,
    compile: function(element, attrs)
    {
      var id = attrs.formInputId;
      var type = attrs.type || 'text';

      var has_model = attrs.hasOwnProperty('model');
      var model = has_model ? attrs.model : "";
      var ngModel = has_model ? attrs.model + '.' + id : id;
      var formName = has_model ? attrs.model + 'Form' : "form";

      var is_required = attrs.hasOwnProperty('required');
      var required = is_required ? ' required ' : ' ';

      var maxlength = attrs.hasOwnProperty('maxlength') ? 
        ' maxlength="' + attrs.maxlength + '" ' : ' ';
      var rows = attrs.hasOwnProperty('rows') ? 
        ' rows="' + attrs.rows + '" ' : ' ';
      var ngOptions = attrs.hasOwnProperty('ngOptions') ? 
        ' ng-options="' + attrs.ngOptions + '" ' : ' ';
      var hint = attrs.hasOwnProperty('hint') ? 
        '<p id="hint_id_' + id + '" class="help-block">' + attrs.hint +'</p>'  : " ";

      var autoFillSync = attrs.hasOwnProperty('autoFillSync') ? ' auto-fill-sync ' : ' ';

      var btcAddressValidation = (type == 'btcAddress') ? ' btc-address ' : ' ';
      if (type == 'btcAddress'){
        maxlength = ' maxlength="34" ';
      }

      // Label
      var htmlText = '<div class="form-group" id="div_id_' + model + '_' + id + '">' +
        '<label class="control-label" for="' + id + '">' + attrs.label + '</label>';
      if (is_required){
        htmlText += '<span class="asteriskField">*</span>';
      }
      htmlText += '</label>';

      // Open input
      htmlText += '<div class="controls">';
      if (type == "textarea"){
        htmlText += '<textarea ';
      } else if (type == "select") {
        htmlText += '<select ';
      } else {
        htmlText += '<input type="' + type + '" ';
      }
      // Common attributes
      htmlText += ' id="id_' + model + '_' + id + '" name="' + id + '" ' +
        'ng-model="' + ngModel + '" ' +
        'class="textinput textInput form-control" ' +
        required + maxlength + rows + ngOptions + 
        autoFillSync + btcAddressValidation  + '>' + hint;

      // Close inputs
      if (type == "textarea"){
        htmlText += '</textarea>';
      } else if (type == "select") {
        // htmlText += '<option ng-repeat="c in categories" value="{{c.id}}">{{c.name}}</option>';
        htmlText += '</select>';
      }

      // Additions
      if (is_required){
        htmlText += '<p ng-show="' + formName + '.' + id + '.$dirty && ' + 
          formName + '.' + id + '.$error.required"' +
          'class="help-block" style="color:red">This field is required.</p>';
      }
      if (type == 'email'){
        htmlText += '<p ng-show="' + formName + '.' + id + '.$dirty && ' + 
          formName + '.' + id + '.$error.email"' +
          'class="help-block" style="color:red">Enter a valid email address.</p>';        
      }
      if (type == 'url'){
        htmlText += '<p ng-show="' + formName + '.' + id + '.$dirty && ' + 
          formName + '.' + id + '.$error.url"' +
          'class="help-block" style="color:red">Enter a valid URL.</p>';        
      }
      if (type == 'btcAddress'){
        htmlText += '<p ng-show="' + formName + '.' + id + '.$dirty && ' + 
          formName + '.' + id + '.$error.btcAddress"' +
          'class="help-block" style="color:red">Enter a valid address.</p>';        
      }
      htmlText += '</div>' +
        '</div>';
      element.replaceWith(htmlText);
    }
  }
});
