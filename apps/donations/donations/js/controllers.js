
function GenericListCtrl($scope, $http, django, type) {
  $scope.django = django;

  $scope.type = type;

  $http.get( django.urlForType(type) ).
    success(function (data){
      $scope.organization_list = data;
    });
  $scope.orderProp = '-id';
}

function OrgListCtrl($scope, $http, django) {

  GenericListCtrl($scope, $http, django, 'validated');
}

function CandidatesListCtrl($scope, $http, django) {

  GenericListCtrl($scope, $http, django, 'candidates');
}

function BlockedListCtrl($scope, $http, django) {

  GenericListCtrl($scope, $http, django, 'blocked');
}

function OrgDetailCtrl($scope, $routeParams, $http, django) {
  $scope.django = django;

  $http.get(django.urls.json + $routeParams.orgId).
    success(function(data) {
      $scope.org = data;
    });
}
