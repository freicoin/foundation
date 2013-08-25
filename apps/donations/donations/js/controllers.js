
function OrgListCtrl($scope, $http) {

  $http.get('/nonprofits/json/').
    success(function (data){
      $scope.organization_list = data;
    });

  $scope.orderProp = '-id';
}

function OrgDetailCtrl($scope, $routeParams, $http) {

  $http.get('/nonprofits/json/' + $routeParams.orgId).
    success(function(data) {
      $scope.org = data;
    });
}
