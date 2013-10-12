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

    var mer = $scope.merchant;
    var callback = function(new_mer) {
      $scope.merchant = new_mer;
      var msg;
      if (mer.validation_state == "validated"){
        msg = "The merchant has been blocked.";
      } else if (mer.validation_state == "blocked") {
        msg = "The merchant is valid again.";
      } else if (mer.validation_state == "candidate") {
        msg = "The merchant has been validated.";
      } else {
        MessageSrv.error("Unkown validation state " + mer.validation_state);
        return;
      }
      MessageSrv.success(msg);
    };
    TradeSrv.validateMerchant(mer, callback);
  };

}]);

module.controller('MerchantEditCtrl', ['$scope', '$routeParams', 'MessageSrv', 'TradeSrv',
                                       function($scope, $routeParams, MessageSrv, TradeSrv)
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

    var callback = function(messages) {
      MessageSrv.success(messages);
      $scope.disableSubmit = false;
    }

    if ($routeParams.merchantId) {
      TradeSrv.updateMerchant($scope.merchant, $routeParams.merchantId, callback);
    } else {
      TradeSrv.createMerchant($scope.merchant, callback);
    }
  };
}]);
