function explorer_link(explorer, type, value){
  return '<a href="' + explorer + '/' + type + '/' + value + '">' + value + '</a>';
}

angular.module('donationFilters', ['django_constants']).
  filter('frc_address', function(django) {
    return function(value) {
      return explorer_link(django.urls.frc_explorer, "address", value);
    };
  }).
  filter('btc_address', function(django) {
    return function(value) {
      return explorer_link(django.urls.btc_explorer, "address", value);
    };
  }).
  filter('frc_tx', function(django) {
    return function(value) {
      return explorer_link(django.urls.frc_explorer, "tx", value);
    };
  }).
  filter('btc_tx', function(django) {
    return function(value) {
      return explorer_link(django.urls.btc_explorer, "tx", value);
    };
  });

