var app = angular.module('foundationApp', ['navCtrls', 'accountsCtrls', 'tradeCtrls', 
                                           'donationsCtrls']);

app.config(['$routeProvider', 
            function($routeProvider) 
{
  $routeProvider.
    when('/', {templateUrl: 'static/html/home.html'}).
    when('/about', {templateUrl: 'static/html/about.html'}).
    when('/copyright', {templateUrl: 'static/html/copyright.html'}).
    when('/register', {templateUrl: 'static/html/accounts/register_form.html', 
                       controller: 'RegisterCtrl'}).
    when('/profile', {templateUrl: 'static/html/accounts/profile_form.html'}).
    when('/trade', {templateUrl: 'static/html/trade/merchant_list.html', 
                    controller: 'MerCategoriesCtrl'}).
    when('/trade/join', {templateUrl: 'static/html/trade/merchant_form.html', 
                         controller: 'MerchantEditCtrl'}).
    when('/trade/edit/:merchantId', {templateUrl: 'static/html/trade/merchant_form.html', 
                                     controller: 'MerchantEditCtrl'}).
    when('/trade/detail/:merchantId', {templateUrl: 'static/html/trade/merchant_detail.html', 
                                       controller: 'MerchantDetailCtrl'}).
    when('/trade/:merchantType', {templateUrl: 'static/html/trade/merchant_list.html', 
                                  controller: 'MerCategoriesCtrl'}).
    when('/donations', {templateUrl: 'static/html/donations/organization_list.html', 
                        controller: 'OrgCategoriesCtrl'}).
    when('/donations/join', {templateUrl: 'static/html/donations/organization_form.html', 
                             controller: 'OrgEditCtrl'}).
    when('/donations/edit/:orgId', {templateUrl: 'static/html/donations/organization_form.html', 
                                    controller: 'OrgEditCtrl'}).
    when('/donations/detail/:orgId', {templateUrl: 'static/html/donations/organization_detail.html', 
                                      controller: 'OrgDetailCtrl'}).
    when('/donations/:orgType', {templateUrl: 'static/html/donations/organization_list.html', 
                                 controller: 'OrgCategoriesCtrl'}).
    otherwise({redirectTo: '/'});
}]);

app.run(['$rootScope', 'SecuritySrv', 
         function($rootScope, SecuritySrv)
{
  $rootScope.security = SecuritySrv;
}]);
