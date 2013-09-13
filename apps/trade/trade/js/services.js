angular.module('tradeServices', ['django_constants'])
  .service('TradeSrv', function ($http, django){

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
      }
    };
  });

