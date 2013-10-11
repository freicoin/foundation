
angular.module('accountsCtrls', ['commonSrvs', 'securitySrv', 'commonDirectives'])
  .controller('LoginCtrl', ['$scope', '$http', 'MessageSrv', 'SecuritySrv',
                                 function($scope, $http, MessageSrv, SecuritySrv){

    $scope.login = function() {
      SecuritySrv.login($scope.username, $scope.password);
    };

    $scope.logout = function() {
      SecuritySrv.logout();
    };
  }])
  .controller('RegisterCtrl', ['$scope', '$http', 'MessageSrv', 'SecuritySrv', 
                                 function($scope, $http, MessageSrv, SecuritySrv){

    $scope.submit = function() {
      SecuritySrv.register($scope.register);
    };
  }]);
