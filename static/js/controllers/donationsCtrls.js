
angular.module('donationsCtrls', ['django_constants', 'donationsSrvs'])
  .controller('OrgCategoriesCtrl', ['$scope', '$routeParams', 'django', 'DonationsSrv', 
                                 function($scope, $routeParams, django, DonationsSrv){

    $scope.django = django;
    $scope.type = $routeParams.orgType ? $routeParams.orgType : 'validated';
    $scope.orderProp = 'id';

    DonationsSrv.getCategories($scope.type, function(categories, org_count){
      $scope.categories_tree = categories;
      $scope.org_count = org_count;
    });
  }])
  .controller('OrgDetailCtrl', ['$scope', '$routeParams', 'django', 'MessageSrv', 'DonationsSrv', 
                                 function($scope, $routeParams, django, MessageSrv, DonationsSrv){

    $scope.django = django;

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
