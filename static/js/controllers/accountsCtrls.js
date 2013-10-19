var module = angular.module('accountsCtrls', ['commonDirs', 'securitySrv']);

module.controller('ShowLoginCtrl', function()
{
  // TODO FIXME this is failing when you godirectly to #/login
  jQuery('#loginModal').modal('show');
});

module.controller('LoginCtrl', ['$scope', 'SecuritySrv',
                                function($scope, SecuritySrv)
{
  var errorCallback = function(data){
    $scope.disableLoginSubmit = false;
    $scope.errorMessages = data;
  }

  var successCallback = function(data){
    $scope.disableLoginSubmit = false;
    jQuery('#loginModal').modal('hide');
  }

  $scope.login = function() {
    $scope.disableLoginSubmit = true;
    SecuritySrv.login($scope.login.username, $scope.login.password, 
                      successCallback, errorCallback);
  };
}]);

module.controller('LogoutCtrl', ['$scope', 'SecuritySrv',
                                function($scope, SecuritySrv)
{
  $scope.logout = function() {
    SecuritySrv.logout();
  };
}]);

module.controller('RegisterCtrl', ['$scope', 'SecuritySrv', 
                                   function($scope, SecuritySrv)
{
  $scope.register = {}
  $scope.submit = function() {
    SecuritySrv.register($scope.register);
  };
}]);

module.controller('PasswordResetCtrl', ['$scope', 'SecuritySrv', 
                                        function($scope, SecuritySrv)
{
  $scope.reset = {}
  $scope.submit = function() {
    SecuritySrv.passwordReset($scope.reset);
  };
}]);

module.controller('ChangePassCtrl', ['$scope', 'SecuritySrv', 
                                   function($scope, SecuritySrv)
{
  $scope.submit = function() {
    SecuritySrv.changePassword($scope.change);
  };
}]);
