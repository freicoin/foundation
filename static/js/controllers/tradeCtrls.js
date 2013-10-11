var module = angular.module('tradeCtrls', ['commonSrvs', 'tradeSrvs']);

module.controller('MerCategoriesCtrl', ['$scope', '$routeParams', 'TradeSrv', 
                                        function($scope, $routeParams, TradeSrv)
{
  $scope.type = $routeParams.merchantType ? $routeParams.merchantType : 'validated';
  $scope.orderProp = 'id';

  TradeSrv.getCategoryTree($scope.type, function(categories, merchant_count){
    $scope.categories_tree = categories;
    $scope.merchant_count = merchant_count;
  });
}]);

module.controller('MerchantDetailCtrl', ['$scope', '$routeParams', 'MessageSrv', 'TradeSrv', 
                                         function($scope, $routeParams, MessageSrv, TradeSrv)
{
  TradeSrv.getMerchant($routeParams.merchantId, function(merchant) {
    $scope.merchant = merchant;
  });

  $scope.validate = function() {
    var msg = null;
    if ($scope.merchant.validation_state == "validated"){
      msg = "The merchant has been blocked.";
    } else if ($scope.merchant.validation_state == "blocked") {
      msg = "The merchant is valid again.";
    } else if ($scope.merchant.validation_state == "candidate") {
      msg = "The merchant has been validated.";
    } else {
      MessageSrv.setMessage("Unkown validation state " + $scope.merchant.validation_state, "error");
      return;
    }
    
    TradeSrv.validateMerchant($routeParams.merchantId, function(merchant) {
      $scope.merchant = merchant;
      MessageSrv.setMessage(msg, "success");
    });
  };
}]);

module.controller('MerchantEditCtrl', ['$scope', '$routeParams', 'TradeSrv',
                                       function($scope, $routeParams, TradeSrv)
{
  if ($routeParams.merchantId) {
    
    TradeSrv.getMerchant($routeParams.merchantId, function(merchant) {
      $scope.merchant = merchant;
    });
  }

  TradeSrv.getCategories(function(categories) {
    $scope.categories = categories;
  });

  $scope.submit = function() {
    $scope.disableSubmit = true;

    var callback = function() {
      $scope.disableSubmit = false;
    }

    if ($routeParams.merchantId) {
      TradeSrv.updateMerchant($scope.merchant, $routeParams.merchantId, callback);
    } else {
      TradeSrv.createMerchant($scope.merchant, callback);
    }
  };
}]);
