var module = angular.module('commonDirectives', []);

// TODO Stop using this when the following issue is fixed:
// https://github.com/angular/angular.js/issues/1460

module.directive('autoFillSync', ['$timeout', function($timeout) {
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
