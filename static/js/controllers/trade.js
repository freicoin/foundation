
angular.module('tradeControllers', ['django_constants', 'commonServices', 'tradeServices'])
  .controller('MerCategoriesCtrl', ['$scope', '$routeParams', 'django', 'TradeSrv', 
                                 function($scope, $routeParams, django, TradeSrv){

    $scope.django = django;
    $scope.type = $routeParams.merchantType ? $routeParams.merchantType : 'validated';
    $scope.orderProp = 'id';

    TradeSrv.getCategoryTree($scope.type, function(categories, merchant_count){
      $scope.categories_tree = categories;
      $scope.merchant_count = merchant_count;
    });
  }])
  .controller('MerchantDetailCtrl', ['$scope', '$routeParams', 'django', 'MessageSrv', 'TradeSrv', 
                                 function($scope, $routeParams, django, MessageSrv, TradeSrv){

    $scope.django = django;

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
  .controller('MerchantEditCtrl', ['$scope', '$routeParams', 'django', 'TradeSrv',
                                   function($scope, $routeParams, django, TradeSrv){

    $scope.django = django;

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
