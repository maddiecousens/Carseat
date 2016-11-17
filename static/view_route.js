function initMap(evt) {

    if ($('#map').length) {
        $('#map').removeAttr('id').addClass('add-map-here');
    }
    else {
    console.log($(this).parent().prevAll());

    console.log($(this).parent().prevAll('.ride').data('startlat'));

    var route = $(this).parent().siblings(".add-map-here").removeClass("add-map-here").attr("id", "map");
    // route.toggle()
    // console.log(route);
    // route.toggle();
    // console.log(route.style.display);
    
    // console.log($(this).parent().parent().parent().siblings().find(".add-map-here"));
    // $(this).parent().parent().parent().siblings().find(".add-map-here").removeClass("add-map-here").attr("id", "map");
    // console.log($(this).parent().parent().parent().parent());
    // $(this).parent().parent().parent().parent().append('<tbody><tr><div id="map"></div></tr></tbody>');

    // console.log($(this).parent().siblings('.ride'));
    // console.log($(this).parent().siblings('.ride').data('startlat'))

    var startLat = $(this).parent().prevAll('.ride').data('startlat')
    var startLng = $(this).parent().prevAll('.ride').data('startlng')
    var endLat = $(this).parent().prevAll('.ride').data('endlat')
    var endLng = $(this).parent().prevAll('.ride').data('endlng')

    var start = {lat: startLat, lng: startLng};
        var end = {lat: endLat, lng: endLng};

        var map = new google.maps.Map(document.getElementById('map'), {
          center: start,
          scrollwheel: false,
          zoom: 7
        });
        var directionsDisplay = new google.maps.DirectionsRenderer({
            map: map
          });

          // Set destination, origin and travel mode.
          var request = {
            destination: end,
            origin: start,
            travelMode: 'DRIVING'
          };

          // Pass the directions request to the directions service.
          var directionsService = new google.maps.DirectionsService();
          directionsService.route(request, function(response, status) {
            if (status == 'OK') {
              // Display the route on the map.
              directionsDisplay.setDirections(response);
            }
          });
}}

        

function addMap(evt) {
    
    $(this).parent().siblings(".add-map-here").removeClass("add-map-here").attr("id", "map");

        // .removeClass("add-map-here");

    // .attr("id", "map");

    // appe nd('<div id="map"></div>');
    console.log('appended map div');

    initMap();

}

$(document).ready(function(){
$('.view-route-btn').on("click", initMap);
});