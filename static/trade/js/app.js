var tradeApp = angular.module('foundationApp', ['django_constants', 'navCtrls', 'tradeControllers', 'tradeServices']).
  config(function($routeProvider, django) {
    $routeProvider.
      when('/', {templateUrl: django.static_urls.home}).
      when('/about', {templateUrl: django.static_urls.about}).
      when('/copyright', {templateUrl: django.static_urls.copyright}).

      when('/trade', {templateUrl: django.static_urls.list, controller: 'CategoriesCtrl'}).
      when('/trade/join', {templateUrl: django.urls.edit, controller: 'MerchantEditCtrl'}).
      when('/trade/edit/:merchantId', {templateUrl: django.static_urls.edit, 
                                       controller: 'MerchantEditCtrl'}).
      when('/trade/detail/:merchantId', {templateUrl: django.static_urls.detail, 
                                         controller: 'MerchantDetailCtrl'}).
      when('/trade/:merchantType', {templateUrl: django.static_urls.list, 
                                    controller: 'CategoriesCtrl'}).
      otherwise({redirectTo: '/'});
  });

// TODO at some point replace django with $cookies
tradeApp.run(function($rootScope, $http, django){
    // set the CSRF token here
    $http.defaults.headers.post['X-CSRFToken'] = django.csrf_token;
    $http.defaults.headers.put['X-CSRFToken'] = django.csrf_token;

    // $http.get('/api/get-current-user').success(function(data){
    //     $rootScope.current_user = data;
    //     $rootScope.current_team = $rootScope.current_user.team;
    // });
    // $http.get('/api/get-current-season').success(function(data){
    //     $rootScope.current_season = data;
    // });
});
