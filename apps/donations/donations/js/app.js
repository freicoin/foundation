angular.module('appDonations', ['django_constants', 'donationFilters']).
  config(function($routeProvider, django) {
    $routeProvider.
      when('/', {templateUrl: django.urls.list, controller: OrgListCtrl}).
      when('/detail/:orgId', {templateUrl: django.urls.detail, controller: OrgDetailCtrl}).
      otherwise({redirectTo: '/'});
  });
