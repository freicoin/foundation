
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


function OrgFormCtrl($scope, $http) {

  $scope.submit = function() {
    alert("aaaa");
    debugger
    $http.post('/nonprofits/join/', {
      org: $scope.org
    }).
      success(function(out_data) {
        debugger
        alert("Thank you for submitting your request!!")
    }).
      error(function(out_data) {
        debugger
        alert("Something went wrong...")
    })
  };
}

