var tradeApp = angular.module('foundationApp', ['django_constants', 'navCtrls', 'utilsFilters',
                                                'accountsCtrls', 'securitySrv',
                                                'tradeCtrls', 'tradeSrvs',
                                                'donationsCtrls', 'donationsSrvs']).
  config(function($routeProvider, django) {
    $routeProvider.
      when('/', {templateUrl: django.static_urls.home}).
      when('/about', {templateUrl: django.static_urls.about}).
      when('/copyright', {templateUrl: django.static_urls.copyright}).
      when('/register', {templateUrl: django.static_urls.register, controller: 'RegisterCtrl'}).

      when('/trade', {templateUrl: django.static_urls.trade_list, controller: 'MerCategoriesCtrl'}).
      when('/trade/join', {templateUrl: django.static_urls.trade_form, controller: 'MerchantEditCtrl'}).
      when('/trade/edit/:merchantId', {templateUrl: django.static_urls.trade_form, 
                                       controller: 'MerchantEditCtrl'}).
      when('/trade/detail/:merchantId', {templateUrl: django.static_urls.trade_detail, 
                                         controller: 'MerchantDetailCtrl'}).
      when('/trade/:merchantType', {templateUrl: django.static_urls.trade_list, 
                                    controller: 'MerCategoriesCtrl'}).

      when('/donations', {templateUrl: django.static_urls.donations_list, 
                          controller: 'OrgCategoriesCtrl'}).
      when('/donations/join', {templateUrl: django.static_urls.donations_form, controller: 'OrgEditCtrl'}).
      when('/donations/edit/:orgId', {templateUrl: django.static_urls.donations_form, 
                                       controller: 'OrgEditCtrl'}).
      when('/donations/detail/:orgId', {templateUrl: django.static_urls.donations_detail, 
                              controller: 'OrgDetailCtrl'}).
      when('/donations/:orgType', {templateUrl: django.static_urls.donations_list, 
                                   controller: 'OrgCategoriesCtrl'}).

      otherwise({redirectTo: '/'});
  });

tradeApp.run(function($rootScope, $http, django, SecuritySrv){
  $rootScope.security = SecuritySrv;
});
