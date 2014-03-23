// usage: log('inside coolFunc', this, arguments);
// paulirish.com/2009/log-a-lightweight-wrapper-for-consolelog/
window.log = function f(){ log.history = log.history || []; log.history.push(arguments); if(this.console) { var args = arguments, newarr; try { args.callee = f.caller } catch(e) {}; newarr = [].slice.call(args); if (typeof console.log === 'object') log.apply.call(console.log, console, newarr); else console.log.apply(console, newarr);}};

// make it safe to use console.log always
(function(a){function b(){}for(var c="assert,count,debug,dir,dirxml,error,exception,group,groupCollapsed,groupEnd,info,log,markTimeline,profile,profileEnd,time,timeEnd,trace,warn".split(","),d;!!(d=c.pop());){a[d]=a[d]||b;}})
(function(){try{console.log();return window.console;}catch(a){return (window.console={});}}());

$(document).ready(function(){
    $("#update-location").click(function(){
       UserGeoLocation.init();
    });
});

// place any jQuery/helper plugins in here, instead of separate, slower script files.
var UserGeoLocation = {
    success_url: "/users/location/add/",

    success: function(position) {
        // let's show a map or do something interesting!
        var data = {
            'csrfmiddlewaretoken': csrf_token,
            'lat': position.coords.latitude,
            'lon': position.coords.longitude
        };
        $.post(UserGeoLocation.success_url, data, function() {
            // server has updated the user location
            location.reload(); // reloads page to user current location.
        })
    },

    error: function() {
        // to be implemented
        console.log("error");
    },

    get_location: function() {
      if (Modernizr.geolocation) {
        navigator.geolocation.getCurrentPosition(this.success, this.error);
      } else {
        // no native support; maybe try a fallback?
        this.error();
      }
    },

    init: function() {
        // asks user for location.
        this.get_location();
    }

};
