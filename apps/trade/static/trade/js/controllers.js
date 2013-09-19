
angular.module('tradeControllers', ['django_constants', 'tradeServices'])
  .controller('CategoriesCtrl', ['$scope', '$routeParams', 'django', 'TradeSrv', 
                                 function($scope, $routeParams, django, TradeSrv){

    $scope.django = django;
    $scope.type = $routeParams.merchantType ? $routeParams.merchantType : 'validated';
    $scope.orderProp = 'id';

    TradeSrv.getCategories($scope.type, function(categories, merchant_count){
      $scope.categories_tree = categories;
      $scope.merchant_count = merchant_count;
    });
  }])
  .controller('MerchantDetailCtrl', ['$scope', '$routeParams', 'django', 'TradeSrv', 
                                 function($scope, $routeParams, django, TradeSrv){

    $scope.django = django;

    TradeSrv.getMerchant($routeParams.merchantId, function(merchant) {
      $scope.merchant = merchant;
    });

    $scope.validate = function() {
      TradeSrv.validateMerchant($routeParams.merchantId, function(merchant) {
        $scope.merchant = merchant;
      });
    };

  }])
  .controller('MerchantEditCtrl', ['$scope', '$routeParams', 'django', 'TradeSrv',
                                   function($scope, $routeParams, django, TradeSrv){

    $scope.django = django;

    var form = $("#merchant_form");
    var actionUrl = form.attr('action');

    if ($routeParams.merchantId) {
    
      actionUrl += $routeParams.merchantId;
      TradeSrv.getMerchant($routeParams.merchantId, function(merchant) {
        $scope.merchant = merchant;
      });
    }

    form.submit(function(e) {
      $("#submit_button").attr('disabled', true)
      $("#submit_wrapper").append('<span>Sending message, please wait... </span>')
      $("#ajax_wrapper").load(
        actionUrl + ' #ajax_wrapper',
        form.serializeArray(),
        function(responseText, responseStatus) {
          $("#submit_button").attr('disabled', false)
        }
      );
      e.preventDefault(); 
    });

  }]);
