var module = angular.module('commonSrvs', []);

module.service('MessageSrv', ['$rootScope', '$timeout',
                              function ($rootScope, $timeout)
{
  $rootScope.isString = function(input) {
    return typeof input === 'string';
  };

  var srv = {};

  srv.clearMessages = function(){
    $rootScope.messages = null;
  };

  srv.setMessages = function (messages, type){

    if( typeof messages === 'string' ) {
      $rootScope.messages = [ messages ];
    } else {
      $rootScope.messages = messages;
    }

    if (!type || type == "info") {
      $rootScope.message_style = "info";
      $timeout(function(){ srv.clearMessages(); }, 4000);
    }
    else if (type == "success") {
      $rootScope.message_style = "success";
      $timeout(function(){ srv.clearMessages(); }, 4000);
    }
    else if (type == "warning") {
      $rootScope.message_style = "warning";
      $timeout(function(){ srv.clearMessages(); }, 6000);
    }
    else if (type == "error") {
      $rootScope.message_style = "danger";
      $timeout(function(){ srv.clearMessages(); }, 10000);
    }

  };

  srv.setMessage = function (message, type){        
    srv.setMessages(message, type);
  };

  return srv;
}]);
