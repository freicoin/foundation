
angular.module('donationsControllers', ['django_constants', 'donationsServices'])
  .controller('CategoriesCtrl', ['$scope', '$routeParams', 'django', 'DonationsSrv', 
                                 function($scope, $routeParams, django, DonationsSrv){

    $scope.django = django;
    $scope.type = $routeParams.orgType ? $routeParams.orgType : 'validated';
    $scope.orderProp = 'id';

    DonationsSrv.getCategories($scope.type, function(categories, org_count){
      $scope.categories_tree = categories;
      $scope.org_count = org_count;
    });
  }])
  .controller('OrgDetailCtrl', ['$scope', '$routeParams', 'django', 'DonationsSrv', 
                                 function($scope, $routeParams, django, DonationsSrv){

    $scope.django = django;

     DonationsSrv.getOrganization($routeParams.orgId, function(org) {
       $scope.org = org;
     });
  }]);
