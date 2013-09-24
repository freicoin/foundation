angular.module('appDonations', ['django_constants', 'donationsControllers', 'donationsServices', 
                                'utilsFilters']).
  config(function($routeProvider, django) {
    $routeProvider.
      when('/', {templateUrl: django.static_urls.donations_list, controller: 'CategoriesCtrl'}).
      when('/:orgType', {templateUrl: django.static_urls.donations_list, controller: 'CategoriesCtrl'}).
      when('/detail/:orgId', {templateUrl: django.static_urls.donations_detail, 
                              controller: 'OrgDetailCtrl'}).
      otherwise({redirectTo: '/'});
  });
