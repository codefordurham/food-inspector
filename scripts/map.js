(function ($) {

    'use strict';

    var map,
        userLocation = {
            // use default coordinates for the city of Durham
            lat: 35.9886,
            lng: -78.9072
        },
        locationLayerPath = "/data/food-locations.geojson",
        createMap = function () {
            var markerLayer = L.mapbox.markerLayer();

            // setup a Code for Durham MapBox account for map?
            map = L.mapbox.map('map', 'tylerpearson.gc56ggok', {zoomControl: false})
                      .setView([userLocation.lat, userLocation.lng], 18);

            new L.Control.Zoom({ position: 'bottomright' }).addTo(map);


            markerLayer.loadURL(locationLayerPath)
                .addTo(map);

            markerLayer.eachLayer(function (layer) {
                var content = '<h1>size: ' + layer.feature.properties.size + '<\/h1>' +
                        '<h2>population: ' + layer.feature.properties.population + '<\/h2>';

                layer.bindPopup(content);
            });

        },
        getUserLocation = function (callbackFunc) {
            var success = function (position) {
                    userLocation.lat = position.coords.latitude;
                    userLocation.lng = position.coords.longitude;
                    if (callbackFunc !== undefined) {
                        callbackFunc();
                    }
                },
                error = function () {
                    console.log("Something went wrong trying to detect user's location.");
                };

            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(success, error);
            } else {
                // add better fallback?
                alert("Please access this site with a browser that supports geolocation");
            }
        },
        init = function () {
            getUserLocation(function () {
                createMap();
            });
        };


    $(document).ready(init);

}(jQuery));
