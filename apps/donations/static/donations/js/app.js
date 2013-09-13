angular.module('appDonations', ['django_constants', 'donationsControllers', 'donationsServices', 
                                'utilsFilters']).
  config(function($routeProvider, django) {
    $routeProvider.
      when('/', {templateUrl: django.urls.list, controller: 'CategoriesCtrl'}).
      when('/:orgType', {templateUrl: django.urls.list, controller: 'CategoriesCtrl'}).
      when('/detail/:orgId', {templateUrl: django.urls.detail, controller: 'OrgDetailCtrl'}).
      otherwise({redirectTo: '/'});
  });
