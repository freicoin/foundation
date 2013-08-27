angular.module('appTrade', ['django_constants']).
  config(function($routeProvider, django) {
    $routeProvider.
      when('/', {templateUrl: django.urls.list, controller: MerchantListCtrl}).
      when('/detail/:merchantId', {templateUrl: django.urls.detail, controller: MerchantDetailCtrl}).
      otherwise({redirectTo: '/'});
  });
