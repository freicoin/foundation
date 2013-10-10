angular.module('securitySrv', ['django_constants', 'commonSrvs'])
  .service('SecuritySrv', function ($rootScope, $http, django, MessageSrv){

    var currentUser = null;

    var srv = {};

    srv.getUser = function(force){
      
      if (!currentUser || force) {
        $http.get(django.urls.current_user)
          .success(function(data){
            currentUser = data;
            // set the CSRF token here
            $http.defaults.headers.post['X-CSRFToken'] = data.csrf_token;
            $http.defaults.headers.put['X-CSRFToken'] = data.csrf_token;
            // Curious group sees everything
            if ($.inArray( 'curious', currentUser.groups) >= 0){
              currentUser.admin = true;
            }
          })
          .error(function(messages){
            MessageSrv.setMessages(messages, "error");
          });
      }
      return currentUser;
    };

    srv.inGroup = function(group){
      if (!currentUser){
        return false;
      }
      return $.inArray( group, currentUser.groups) >= 0
      // Admin sees everything
        || currentUser.admin 
      // Curious group sees everything
        || $.inArray( 'curious', currentUser.groups) >= 0;
    };

    srv.login = function(username, password){
      var loginData = {"username": username, "password": password};
      $http.post(django.urls.login, loginData)
        .success(function(data){
          srv.getUser(true);
        })
        .error(function(messages){
          MessageSrv.setMessages(messages, "error");
        });
    };

    srv.logout = function(){
      $http.post(django.urls.logout, {})
        .success(function(data){
          srv.getUser(true);
        })
        .error(function(messages){
          MessageSrv.setMessages(messages, "error");
        });
    };

    srv.register = function(register){
      // var registerData = {"register": register,
      //                     "recaptcha": vcRecaptchaService.data()};

      $http.post(django.urls.register, register)
        .success(function(data){
          MessageSrv.setMessages("You've registered as " + register.username 
                                 + ". Please, login.", "success");
        })
        .error(function(messages){
          MessageSrv.setMessages(messages, "error");
          // In case of a failed validation you need to reload the
          // captcha because each challenge can be checked just once
          // vcRecaptchaService.reload();
        });
    };
    
    srv.getUser(true);
    return srv;
  });

