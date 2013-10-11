var module = angular.module('tradeSrvs', ['commonSrvs']);

module.service('TradeSrv', ['$http', 'MessageSrv',
                            function ($http, MessageSrv)
{
  var categories_short = [];

  var categories = {
    all: [],
    validated: [],
    candidates: [],
    blocked: []
  };
  var merchantCount = {
    all: 0,
    validated: 0,
    candidates: 0,
    blocked: 0
  };

  var srv = {};

  srv.getCategories = function (callback){

    if (categories_short.length > 0){
      callback(categories_short);
    } else {

      $http.get("api/trade/categories")
        .success(function(data) {
          categories_short = data;
          callback(categories_short);
        });
    }
  };

  srv.getCategoryTree = function (merchant_type, callback){

    if (merchantCount[merchant_type] > 0){
      callback(categories[merchant_type], merchantCount[merchant_type]);
    } else {

      $http.get("api/trade/categories/tree/" + merchant_type)
        .success(function(data) {

          categories[merchant_type] = data;
          merchantCount[merchant_type] = 0;            
          for (var i=0; i < data.length; i++){
            merchantCount[merchant_type] += data[i].inner_merchants;
          }

          callback(categories[merchant_type], merchantCount[merchant_type]);
        });
    }
  };

  srv.getMerchant = function(merchantId, callback){
    $http.get("api/trade/merchant/" + merchantId).success(callback);
  };

  srv.createMerchant = function(merchant, callback){

    var successCallback = function(messages) {
      MessageSrv.setMessages(messages, "success");
      callback();
    }
    var errorCallback = function(messages, status) {
      MessageSrv.setMessages(messages, "error");
      callback();
    }

    if (merchant == null) {
      errorCallback("The merchant cannot be empty!")
    } else {
      $http.post("api/trade/merchant/create/", merchant)
        .success(successCallback)
        .error(errorCallback);
    }
  };

  srv.updateMerchant = function(merchant, merchantId, callback){
    
    var successCallback = function(messages) {
      MessageSrv.setMessages(messages, "success");
      callback();
    }
    var errorCallback = function(messages, status) {
      MessageSrv.setMessages(messages, "error");
      callback();
    }

    if (merchant == null) {
      errorCallback("The merchant cannot be empty!")
    } else {
      $http.put("api/trade/merchant/edit/" + merchantId, merchant)
        .success(successCallback)
        .error(errorCallback);
    }
  };

  srv.validateMerchant = function(merchantId, callback){

    var errorCallback = function(messages, status) {
      MessageSrv.setMessages(messages, "error");
    }

    $http.put("api/trade/merchant/validate/" + merchantId, {})
      .success(callback)
      .error(errorCallback);
  };

  return srv;
}]);

