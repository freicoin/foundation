angular.module('tradeSrvs', ['django_constants', 'commonSrvs'])
  .service('TradeSrv', function ($http, django, MessageSrv){

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

    return {
      getCategories: function (callback){

        if (categories_short.length > 0){
            callback(categories_short);
        } else {

          $http.get(django.urls.trade_categories)
            .success(function(data) {
              categories_short = data;
              callback(categories_short);
            });
        }
      },
      getCategoryTree: function (merchant_type, callback){

        if (merchantCount[merchant_type] > 0){
            callback(categories[merchant_type], merchantCount[merchant_type]);
        } else {

          $http.get(django.urls.trade_category_tree + merchant_type)
            .success(function(data) {

              categories[merchant_type] = data;
              merchantCount[merchant_type] = 0;            
              for (var i=0; i < data.length; i++){
                merchantCount[merchant_type] += data[i].inner_merchants;
              }

              callback(categories[merchant_type], merchantCount[merchant_type]);
            });
        }
      },
      getMerchant: function(merchantId, callback){
          $http.get(django.urls.trade_merchant_detail + merchantId).success(callback);
      },
      createMerchant: function(merchant, callback){

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
          $http.post(django.urls.trade_merchant_edit, merchant)
            .success(successCallback)
            .error(errorCallback);
        }
      },
      updateMerchant: function(merchant, merchantId, callback){
        
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
          $http.put(django.urls.trade_merchant_edit + merchantId + '/', merchant)
            .success(successCallback)
            .error(errorCallback);
        }

        
      },
      validateMerchant: function(merchantId, callback){

        var errorCallback = function(messages, status) {
          MessageSrv.setMessages(messages, "error");
          callback();
        }

        $http.put(django.urls.trade_merchant_validate + merchantId + '/', {})
          .success(callback)
          .error(errorCallback);
      }
    };
  });

