angular.module('donationsServices', ['django_constants', 'commonServices'])
  .service('DonationsSrv', function ($http, django, MessageSrv){

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
      getCategories: function (org_type, callback){

        if (orgCount[org_type] > 0){
            callback(categories[org_type], orgCount[org_type]);
        } else {

          $http.get(django.urls.donations_category_tree + org_type)
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
          $http.get(django.urls.donations_organization_detail + orgId).success(callback);
      },
      validateOrganization: function(orgId, callback){

        var errorCallback = function(messages, status) {
          MessageSrv.setMessages(messages, "error");
          callback();
        }

        $http.put(django.urls.donations_organization_validate + orgId + '/', {})
          .success(callback)
          .error(errorCallback);
      }
    };
  });
