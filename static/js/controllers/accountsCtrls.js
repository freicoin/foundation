
angular.module('accountsCtrls', ['django_constants', 'commonSrvs', 'securitySrv', 'commonDirectives'])
  .controller('LoginCtrl', ['$scope', '$http', 'django', 'MessageSrv', 'SecuritySrv',
                                 function($scope, $http, django, MessageSrv, SecuritySrv){

    $scope.login = function() {
      SecuritySrv.login($scope.username, $scope.password);
    };

    $scope.logout = function() {
      SecuritySrv.logout();
    };
  }])
  .controller('RegisterCtrl', ['$scope', '$http', 'django', 'MessageSrv', 'SecuritySrv', 
                                 function($scope, $http, django, MessageSrv, SecuritySrv){

    $scope.submit = function() {
      SecuritySrv.register($scope.register);
    };
  }]);
