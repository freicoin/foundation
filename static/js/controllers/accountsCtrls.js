
angular.module('accountsCtrls', ['django_constants', 'commonSrvs', 'commonDirectives', 'vcRecaptcha'])
  .controller('LoginCtrl', ['$scope', '$http', 'django', 'MessageSrv', 
                                 function($scope, $http, django, MessageSrv){

    $scope.login = function() {
      
      var loginData = {"username": $scope.username, "password": $scope.password};
      $http.post(django.urls.login, loginData)
        .success(function(data){
          window.location = "http://127.0.0.1:8000/";
        })
        .error(function(messages){
          MessageSrv.setMessages(messages, "error");
        });
    };

    $scope.logout = function() {
      
      var loginData = {"username": $scope.username, "password": $scope.password};
      $http.post(django.urls.logout, {})
        .success(function(data){
          window.location = "http://127.0.0.1:8000/";
        })
        .error(function(messages){
          MessageSrv.setMessages(messages, "error");
        });
    };


  }])
  .controller('RegisterCtrl', ['$scope', '$http', 'django', 'vcRecaptchaService', 'MessageSrv', 
                                 function($scope, $http, django, vcRecaptchaService, MessageSrv){

    $scope.submit = function() {

      var registerData = {"register": $scope.register,
                          "recaptcha": vcRecaptchaService.data()};

      $http.post(django.urls.register, registerData)
        .success(function(data){
          MessageSrv.setMessages("You've registered as " + data.username 
                                 + ". Please, login.", "success");
          // window.location = "http://127.0.0.1:8000/";
        })
        .error(function(messages){
          MessageSrv.setMessages(messages, "error");
          // In case of a failed validation you need to reload the
          // captcha because each challenge can be checked just once
          // vcRecaptchaService.reload();
        });
    };

  }]);
