
function MerchantListCtrl($scope, $http, django) {
  $scope.django = django;

  $http.get(django.urls.json).
    success(function (data){
      $scope.categories_tree = data;
    });

  $scope.orderProp = 'id';
}

function MerchantDetailCtrl($scope, $routeParams, $http, django) {
  $scope.django = django;

  $http.get(django.urls.json + $routeParams.merchantId).
    success(function(data) {
      $scope.merchant = data;
    });
}
