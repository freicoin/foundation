
function OrgListCtrl($scope, $http) {

  $http.get('/nonprofits/json/').
    success(function (data){
      $scope.organization_list = data;
    });

  $scope.orderProp = '-id';
  $scope.user_authenticated = user_authenticated;
}

function OrgDetailCtrl($scope, $routeParams, $http) {

  $http.get('/nonprofits/json/' + $routeParams.orgId).
    success(function(data) {
      $scope.org = data;
    });
  $scope.user_authenticated = user_authenticated;
  $scope.user_id = user_id;
}
