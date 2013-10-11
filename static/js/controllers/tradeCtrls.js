
angular.module('tradeCtrls', ['commonSrvs', 'tradeSrvs'])
  .controller('MerCategoriesCtrl', ['$scope', '$routeParams', 'TradeSrv', 
                                 function($scope, $routeParams, TradeSrv){

    $scope.type = $routeParams.merchantType ? $routeParams.merchantType : 'validated';
    $scope.orderProp = 'id';

    TradeSrv.getCategoryTree($scope.type, function(categories, merchant_count){
      $scope.categories_tree = categories;
      $scope.merchant_count = merchant_count;
    });
  }])
  .controller('MerchantDetailCtrl', ['$scope', '$routeParams', 'MessageSrv', 'TradeSrv', 
                                 function($scope, $routeParams, MessageSrv, TradeSrv){

    TradeSrv.getMerchant($routeParams.merchantId, function(merchant) {
      $scope.merchant = merchant;
    });

    $scope.validate = function() {
      var msg = null;
      if ($scope.merchant.validated_by){
        msg = "The merchant has been blocked."
      } else if ($scope.merchant.validated) {
        msg = "The merchant is valid again."
      } else {
        msg = "The merchant has been validated."
      }
         
      TradeSrv.validateMerchant($routeParams.merchantId, function(merchant) {
        $scope.merchant = merchant;
        MessageSrv.setMessage(msg, "success");
      });
    };

  }])
  .controller('MerchantEditCtrl', ['$scope', '$routeParams', 'TradeSrv',
                                   function($scope, $routeParams, TradeSrv){

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
