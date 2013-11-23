(function ($) {

    'use strict';

    var map,
        userLocation = {
            // use default coordinates for the city of Durham
            lat: 35.9886,
            lng: -78.9072
        },
        locationLayerPath = "/data/raw.json",
        createMap = function () {
            // setup a Code for Durham MapBox account for map?
            map = L.mapbox.map('map', 'tylerpearson.gc56ggok', {zoomControl: false})
                      .setView([userLocation.lat, userLocation.lng], 17);

            new L.Control.Zoom({ position: 'bottomright' }).addTo(map);

            var locationLayer = L.mapbox.markerLayer()
                .loadURL(locationLayerPath)
                .addTo(map);

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
