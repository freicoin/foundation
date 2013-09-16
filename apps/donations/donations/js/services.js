angular.module('donationsServices', ['django_constants'])
  .service('DonationsSrv', function ($http, django){

      var categories = {
        validated: [],
        candidates: [],
        blocked: []
      };
      var orgCount = {
        validated: 0,
        candidates: 0,
        blocked: 0
      };

    return {
      getCategories: function (org_type, callback){

        if (orgCount[org_type] > 0){
            callback(categories[org_type], orgCount[org_type]);
        } else {

          $http.get(django.urls.json + org_type)
            .success(function(data) {

              categories[org_type] = data;
              orgCount[org_type] = 0;            
              for (var i=0; i < data.length; i++){
                orgCount[org_type] += data[i].inner_orgs;
              }

              callback(categories[org_type], orgCount[org_type]);
            });
        }
      },
      getOrganization: function(orgId, callback){
          $http.get(django.urls.json + orgId).success(callback);
      }
    };
  });

