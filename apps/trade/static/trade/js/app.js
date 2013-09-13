angular.module('appTrade', ['django_constants', 'tradeControllers', 'tradeServices']).
  config(function($routeProvider, django) {
    $routeProvider.
      when('/', {templateUrl: django.urls.list, controller: 'CategoriesCtrl'}).
      when('/:merchantType', {templateUrl: django.urls.list, controller: 'CategoriesCtrl'}).
      when('/detail/:merchantId', {templateUrl: django.urls.detail, controller: 'MerchantDetailCtrl'}).
      otherwise({redirectTo: '/'});
  });
