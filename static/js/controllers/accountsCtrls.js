var module = angular.module('accountsCtrls', ['commonDirs', 'securitySrv']);

module.controller('LoginCtrl', ['$scope', '$http', 'SecuritySrv',
                                function($scope, $http, SecuritySrv)
{
  $scope.login = function() {
    SecuritySrv.login($scope.username, $scope.password);
  };

  $scope.logout = function() {
    SecuritySrv.logout();
  };
}]);

module.controller('RegisterCtrl', ['$scope', '$http', 'SecuritySrv', 
                                   function($scope, $http, SecuritySrv)
{
  $scope.submit = function() {
    SecuritySrv.register($scope.register);
  };
}]);
