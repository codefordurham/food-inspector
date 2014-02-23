'use strict';


angular.module('durhamRestaurants', [
    'ngRoute',
    'leaflet-directive',
    'durhamRestaurants.controllers'
]).config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/', {templateUrl: 'partials/map.html', controller: 'EstablishmentsController'});
  $routeProvider.when('/details', {templateUrl: 'partials/details.html', controller: 'DetailsController'});
  $routeProvider.otherwise({redirectTo: '/'});
}]);
