var module = angular.module('tradeSrvs', ['commonSrvs']);

module.service('TradeSrv', ['$http', 'MessageSrv',
                            function ($http, MessageSrv)
{
  var categories_short = [];

  var categories = {
    all: [],
    validated: [],
    candidate: [],
    blocked: []
  };
  var merchantCount = {
    all: 0,
    validated: 0,
    candidate: 0,
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

  srv.getCategoryTree = function (merchant_type, callback, force){

    if (force || merchantCount[merchant_type] == 0){

      $http.get("api/trade/categories/tree/" + merchant_type)
        .success(function(data) {

          categories[merchant_type] = data;
          merchantCount[merchant_type] = 0;            
          for (var i=0; i < data.length; i++){
            merchantCount[merchant_type] += data[i].inner_merchants;
          }

          callback(categories[merchant_type], merchantCount[merchant_type]);
        });
    } else {
      callback(categories[merchant_type], merchantCount[merchant_type]);
    }
  };

  srv.getMerchant = function(merchantId, callback){
    $http.get("api/trade/merchant/" + merchantId).success(callback);
  };

  var successReloadCallback = function(validation_state, callback) {
    return function(data) {
      srv.getCategoryTree(validation_state, function(){}, true);
      callback(data);
    }
  };

  srv.createMerchant = function(merchant, callback){

    if (merchant == null) {
      MessageSrv.setMessages("The merchant cannot be empty!", "error");
    } else {
      $http.post("api/trade/merchant/create/", merchant)
        .success(successReloadCallback("candidate", callback))
        .error(MessageSrv.errorCallback(callback));
    }
  };

  srv.updateMerchant = function(merchant, merchantId, callback){
    
    if (merchant == null) {
      MessageSrv.setMessages("The merchant cannot be empty!", "error");
    } else {
      $http.put("api/trade/merchant/edit/" + merchantId, merchant)
        .success(successReloadCallback(merchant.validation_state, callback))
        .error(MessageSrv.errorCallback(callback));
    }
  };

  srv.validateMerchant = function(merchant, callback){

    var validateReloadCallback = function(new_mer){
      srv.getCategoryTree(merchant.validation_state, function(){}, true);
      srv.getCategoryTree(new_mer.validation_state, function(){}, true);
      callback(new_mer);
    }
    $http.put("api/trade/merchant/validate/" + merchant.id, {})
      .success(validateReloadCallback)
      .error(MessageSrv.errorCallbackSimple);
  };

  return srv;
}]);

