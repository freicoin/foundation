var module = angular.module('validationDirectives', []);

module.directive('btcAddress', function() {
  return {
    require: 'ngModel',
    link: function(scope, elm, attrs, ctrl) {
      ctrl.$parsers.unshift(function(viewValue) {

        	// Trim address
        viewValue = viewValue.replace(/^\s+/, "").replace(/\s+$/, "");
        if (!viewValue.length){
          ctrl.$setValidity('btcAddress', true);
        } else {
	        try {
            var pubKeyHash = Bitcoin.Address.decodeString(viewValue);
            // it is valid
            ctrl.$setValidity('btcAddress', true);

          } catch (e) {
            // it is invalid, return undefined (no model update)
            ctrl.$setValidity('btcAddress', false);
          }
        }
        return viewValue;
      });
    }
  };
});
