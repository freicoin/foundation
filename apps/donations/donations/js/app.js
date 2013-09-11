angular.module('appDonations', ['django_constants', 'utilsFilters']).
  config(function($routeProvider, django) {
    $routeProvider.
      when('/', {templateUrl: django.urls.list, controller: OrgListCtrl}).
      when('/candidates', {templateUrl: django.urls.list, controller: CandidatesListCtrl}).
      when('/blocked', {templateUrl: django.urls.list, controller: BlockedListCtrl}).
      when('/detail/:orgId', {templateUrl: django.urls.detail, controller: OrgDetailCtrl}).
      otherwise({redirectTo: '/'});
  });
