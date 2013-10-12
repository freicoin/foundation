var module = angular.module('donationsSrvs', ['commonSrvs']);

module.service('DonationsSrv', ['$http', 'MessageSrv',
                            function ($http, MessageSrv)
{
  var categories_short = [];

  var categories = {
    all: [],
    validated: [],
    candidate: [],
    blocked: []
  };
  var orgCount = {
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

      $http.get("api/donations/categories")
        .success(function(data) {
          categories_short = data;
          callback(categories_short);
        });
    }
  };

  srv.getCategoryTree = function (org_type, callback, force){

    if (force || orgCount[org_type] == 0){

      $http.get("api/donations/categories/tree/" + org_type)
        .success(function(data) {

          categories[org_type] = data;
          orgCount[org_type] = 0;
          for (var i=0; i < data.length; i++){
            orgCount[org_type] += data[i].inner_organizations;
          }

          callback(categories[org_type], orgCount[org_type]);
        });
    } else {
      callback(categories[org_type], orgCount[org_type]);
    }
  };

  srv.getOrganization = function(orgId, callback){
    $http.get("api/donations/organization/" + orgId).success(callback);
  };

  var successReloadCallback = function(validation_state, callback) {
    return function(data) {
      srv.getCategoryTree(validation_state, function(){}, true);
      callback(data);
    }
  };

  srv.createOrganization = function(org, callback){

    if (org == null) {
      MessageSrv.error("The organization cannot be empty!");
    } else {
      $http.post("api/donations/organization/create/", org)
        .success(successReloadCallback("candidate", callback))
        .error(MessageSrv.errorCallback(callback));
    }
  };

  srv.updateOrganization = function(org, orgId, callback){
    
    if (org == null) {
      MessageSrv.error("The organization cannot be empty!");
    } else {
      $http.put("api/donations/organization/edit/" + orgId, org)
        .success(successReloadCallback(org.validation_state, callback))
        .error(MessageSrv.errorCallback(callback));
    }
  };

  srv.validateOrganization = function(org, callback){

    var validateReloadCallback = function(new_org){
      srv.getCategoryTree(org.validation_state, function(){}, true);
      srv.getCategoryTree(new_org.validation_state, function(){}, true);
      callback(new_org);
    }
    $http.put("api/donations/organization/validate/" + org.id, {})
      .success(validateReloadCallback)
      .error(MessageSrv.errorCallbackSimple);
  };

  return srv;
}]);
