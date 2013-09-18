angular.module('appTrade', ['django_constants', 'tradeControllers', 'tradeServices']).
  config(function($routeProvider, django) {
    $routeProvider.
      when('/', {templateUrl: django.urls.list, controller: 'CategoriesCtrl'}).
      when('/join', {templateUrl: django.urls.edit, controller: 'MerchantEditCtrl'}).
      when('/edit/:merchantId', {templateUrl: django.urls.edit, controller: 'MerchantEditCtrl'}).
      when('/detail/:merchantId', {templateUrl: django.urls.detail, controller: 'MerchantDetailCtrl'}).
      when('/:merchantType', {templateUrl: django.urls.list, controller: 'CategoriesCtrl'}).
      otherwise({redirectTo: '/aaa'});
  });
