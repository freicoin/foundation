
function MerchantListCtrl($scope, $http, django) {

  $http.get(django.urls.json).
    success(function (data){
      $scope.merchant_list = data;
    });

  $scope.orderProp = '-id';
  $scope.django = django;
}

function MerchantDetailCtrl($scope, $routeParams, $http, django) {

  $http.get(django.urls.json + $routeParams.merchantId).
    success(function(data) {
      $scope.merchant = data;
    });
  $scope.django = django;
}
