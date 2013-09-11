angular.module('appTrade', ['django_constants']).
  config(function($routeProvider, django) {
    $routeProvider.
      when('/', {templateUrl: django.urls.list, controller: MerchantListCtrl}).
      when('/candidates', {templateUrl: django.urls.list, controller: CandidatesListCtrl}).
      when('/blocked', {templateUrl: django.urls.list, controller: BlockedListCtrl}).
      when('/detail/:merchantId', {templateUrl: django.urls.detail, controller: MerchantDetailCtrl}).
      otherwise({redirectTo: '/'});
  });
