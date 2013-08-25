
function OrgListCtrl($scope, $http, django) {

  $http.get(django.urls.json).
    success(function (data){
      $scope.organization_list = data;
    });

  $scope.orderProp = '-id';
  $scope.django = django;
}

function OrgDetailCtrl($scope, $routeParams, $http, django) {

  $http.get(django.urls.json + $routeParams.orgId).
    success(function(data) {
      $scope.org = data;
    });
  $scope.django = django;
}
