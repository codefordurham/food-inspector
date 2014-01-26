(function ($) {

    'use strict';

    var map,
        userLocation = {
            // use default coordinates for the city of Durham
            lat: 35.9886,
            lng: -78.9072
        },
        locationLayerPath = 'https://107.170.26.176/api/v1/establishment/?format=geojson&est_type=1&ordering=-update_date&within=-78.90999913215637,35.992712509370044,-78.889399766922,35.99845018569175',
        addMarker = function (lat, lng, markerHexColor, markerSymbol, markerSize) {
            var markerInfo = {
                    type: 'Feature',
                    geometry: {
                        type: 'Point',
                        coordinates: [lng, lat]
                    },
                    properties: {}
                };

            // clean this up at some point
            if (markerHexColor !== undefined) {
                markerInfo.properties['marker-color'] = markerHexColor;
            }

            if (markerSymbol !== undefined) {
                markerInfo.properties['marker-symbol'] = markerSymbol;
            }

            if (markerSize !== undefined) {
                markerInfo.properties['marker-size'] = markerSize;
            }

            L.mapbox.markerLayer(markerInfo).addTo(map);
        },
        moveMapCenter = function (lat, lng) {
            map.panTo([lat, lng]);
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

            navigator.geolocation.getCurrentPosition(success, error);
        },
        initMap = function () {
            var markerLayer = L.mapbox.markerLayer();

            // setup a Code for Durham MapBox account for map?
            map = L.mapbox.map('map', 'tylerpearson.gc56ggok', {zoomControl: false})
                      .setView([userLocation.lat, userLocation.lng], 17);

            new L.Control.Zoom({ position: 'bottomright' }).addTo(map);

            markerLayer.loadURL(locationLayerPath)
                .addTo(map);

            markerLayer.on('click', function (e) {
                e.layer.unbindPopup();
                var latlng = e.latlng;
                var popup = L.popup();
                var content = [
                    '<div>',
                    '<h2>' + e.layer.feature.properties.premise_name + '</h2>',
                    '<strong>Inspection Score:</strong><br/>',
                    '<strong>Yelp Score:</strong><br/>',
                    '</div>'
                ].join('\n');
                popup.setLatLng(latlng).setContent(content);
                map.panTo(latlng);
                popup.openOn(map);
            });

            map.on('moveend', function(e) {
                console.log(map.getBounds());
                console.log(map.getBounds().toBBoxString());
            });

        },
        init = function () {
            initMap();

            if (navigator.geolocation) {
                getUserLocation(function () {
                    // add a marker for the user's detected location
                    addMarker(userLocation.lat, userLocation.lng, '#41b649', 'star', 'large');

                    // move the center of map to user's detected location
                    moveMapCenter(userLocation.lat, userLocation.lng);
                });
            } else {
                alert("To automatically view locations nearby, please access this site with a browser that supports geolocation");
            }
        };


    $(document).ready(init);

}(jQuery));
