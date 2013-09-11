
function GenericListCtrl($scope, $http, django, type) {
  $scope.django = django;

  $scope.type = type;

  $http.get( django.urlForType(type) ).
    success(function (data){
      $scope.categories_tree = data;
    });
  $scope.orderProp = 'id';
}

function MerchantListCtrl($scope, $http, django) {

  GenericListCtrl($scope, $http, django, 'validated');
}

function CandidatesListCtrl($scope, $http, django) {

  GenericListCtrl($scope, $http, django, 'candidates');
}

function BlockedListCtrl($scope, $http, django) {

  GenericListCtrl($scope, $http, django, 'blocked');
}

function MerchantDetailCtrl($scope, $routeParams, $http, django) {
  $scope.django = django;

  $http.get(django.urls.json + $routeParams.merchantId).
    success(function(data) {
      $scope.merchant = data;
    });
}
