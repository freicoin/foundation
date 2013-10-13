var module = angular.module('accountsCtrls', ['commonDirs', 'securitySrv']);

module.controller('LoginCtrl', ['$rootScope', '$scope', '$http', 'SecuritySrv',
                                function($rootScope, $scope, $http, SecuritySrv)
{
  $scope.login = function() {
    SecuritySrv.login($scope.username, $scope.password);
    $rootScope.show_login = false;
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

module.controller('ChangePassCtrl', ['$scope', '$http', 'SecuritySrv', 
                                   function($scope, $http, SecuritySrv)
{
  $scope.submit = function() {
    SecuritySrv.changePassword($scope.change);
  };
}]);
