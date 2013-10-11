angular.module('donationsSrvs', ['commonSrvs'])
  .service('DonationsSrv', ['$http', 'MessageSrv',
                            function ($http, MessageSrv){

    var categories_short = [];

    var categories = {
      all: [],
      validated: [],
      candidates: [],
      blocked: []
    };
    var orgCount = {
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

          $http.get("api/donations/categories")
            .success(function(data) {
              categories_short = data;
              callback(categories_short);
            });
        }
      },
      getCategoryTree: function (org_type, callback){

        if (orgCount[org_type] > 0){
            callback(categories[org_type], orgCount[org_type]);
        } else {

          $http.get("api/donations/categories/tree/" + org_type)
            .success(function(data) {

              categories[org_type] = data;
              orgCount[org_type] = 0;
              for (var i=0; i < data.length; i++){
                orgCount[org_type] += data[i].inner_organizations;
              }

              callback(categories[org_type], orgCount[org_type]);
            });
        }
      },
      getOrganization: function(orgId, callback){
          $http.get("api/donations/organization/" + orgId).success(callback);
      },
      createOrganization: function(org, callback){

        var successCallback = function(messages) {
          MessageSrv.setMessages(messages, "success");
          callback();
        }
        var errorCallback = function(messages, status) {
          MessageSrv.setMessages(messages, "error");
          callback();
        }

        if (org == null) {
          errorCallback("The organization cannot be empty!")
        } else {
          $http.post("api/donations/organization/create/", org)
            .success(successCallback)
            .error(errorCallback);
        }
      },
      updateOrganization: function(org, orgId, callback){
        
        var successCallback = function(messages) {
          MessageSrv.setMessages(messages, "success");
          callback();
        }
        var errorCallback = function(messages, status) {
          MessageSrv.setMessages(messages, "error");
          callback();
        }

        if (org == null) {
          errorCallback("The organization cannot be empty!")
        } else {
          $http.put("api/donations/organization/edit/" + orgId, org)
            .success(successCallback)
            .error(errorCallback);
        }

        
      },
      validateOrganization: function(orgId, callback){

        var errorCallback = function(messages, status) {
          MessageSrv.setMessages(messages, "error");
        }

        $http.put("api/donations/organization/validate/" + orgId, {})
          .success(callback)
          .error(errorCallback);
      }
    };
  }]);
