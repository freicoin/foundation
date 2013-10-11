var module = angular.module('donationsCtrls', ['commonDirs', 'validationDirs', 
                                               'commonSrvs', 'donationsSrvs']);

module.controller('OrgCategoriesCtrl', ['$scope', '$routeParams', 'DonationsSrv', 
                                        function($scope, $routeParams, DonationsSrv)
{
  $scope.type = $routeParams.orgType ? $routeParams.orgType : 'validated';
  $scope.orderProp = 'id';

  DonationsSrv.getCategoryTree($scope.type, function(categories, org_count){
    $scope.categories_tree = categories;
    $scope.org_count = org_count;
  });
}]);

module.controller('OrgDetailCtrl', ['$scope', '$routeParams', 'MessageSrv', 'DonationsSrv', 
                                    function($scope, $routeParams, MessageSrv, DonationsSrv)
{
  DonationsSrv.getOrganization($routeParams.orgId, function(org) {
    $scope.org = org;
  });

  $scope.validate = function() {
    var msg = null;
    if ($scope.org.validated_by){
      msg = "The organization has been blocked."
    } else if ($scope.org.validated) {
      msg = "The organization is valid again."
    } else {
      msg = "The organization has been validated."
    }
    
    DonationsSrv.validateOrganization($routeParams.orgId, function(org) {
      $scope.org = org;
      MessageSrv.setMessage(msg, "success");
    });
  };
}]);

module.controller('OrgEditCtrl', ['$scope', '$routeParams', 'MessageSrv', 'DonationsSrv', 
                                  function($scope, $routeParams, MessageSrv, DonationsSrv)
{
  if ($routeParams.orgId) {
    
    DonationsSrv.getOrganization($routeParams.orgId, function(org) {
      $scope.org = org;
    });
  }

  DonationsSrv.getCategories(function(categories) {
    $scope.categories = categories;
  });

  $scope.submit = function() {
    
    $scope.disableSubmit = true;

    var callback = function() {
      $scope.disableSubmit = false;
    }

    if ($routeParams.orgId) {
      DonationsSrv.updateOrganization($scope.org, $routeParams.orgId, callback);
    } else {
      DonationsSrv.createOrganization($scope.org, callback);
    }
  };
}]);
