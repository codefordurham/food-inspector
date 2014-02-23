'use strict';


angular.module('durhamRestaurants.controllers', []).
    controller("EstablishmentsController", ['$scope', '$http', function($scope, $http) {
        angular.extend($scope, {
            durham: {
                lat: 35.9956,
                lng: -78.9072,
                zoom: 16
            },
            defaults: {
                scrollWheelZoom: false
            }
        });

        // Get the countries geojson data from a JSON
        $http.get("http://107.170.26.176/api/v1/establishment/?format=geojson&est_type=1&ordering=-update_date&within=-78.90999913215637,35.992712509370044,-78.889399766922,35.99845018569175").success(function(data, status) {
            angular.extend($scope, {
                geojson: {
                    data: data,
                }
            });
        });
    }]).

    controller("DetailsController", ['$scope', '$http', function($scope, $http) {
        // Get details from API
    }]);
