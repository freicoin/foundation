angular.module('tradeServices', ['django_constants', 'commonServices'])
  .service('TradeSrv', function ($http, django, MessageSrv){

      var categories = {
        validated: [],
        candidates: [],
        blocked: []
      };
      var merchantCount = {
        validated: 0,
        candidates: 0,
        blocked: 0
      };

    return {
      getCategories: function (merchant_type, callback){

        if (merchantCount[merchant_type] > 0){
            callback(categories[merchant_type], merchantCount[merchant_type]);
        } else {

          $http.get(django.urls.json + merchant_type)
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
          $http.get(django.urls.json + merchantId).success(callback);
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
          $http.post(django.urls.json_edit, merchant)
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
          $http.put(django.urls.json_edit + merchantId + '/', merchant)
            .success(successCallback)
            .error(errorCallback);
        }

        
      },
      validateMerchant: function(merchantId, callback){

        var errorCallback = function(messages, status) {
          MessageSrv.setMessages(messages, "error");
          callback();
        }

        $http.put(django.urls.validate + merchantId + '/', {})
          .success(callback)
          .error(errorCallback);
      }
    };
  });

