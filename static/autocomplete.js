

// Create variables
var placeSearch, autocomplete, autocomplete2;

// Call initAutocomplete once window has loaded
google.maps.event.addDomListener(window, "load", initAutocomplete);

// Attributes being pulled from the .getPlace() object. 
var componentForm = {
  // street_number: 'long_name',
  // route: 'long_name',
  locality: 'long_name',
  administrative_area_level_1: 'short_name',
  postal_code: 'short_name'
};



// When the user selects an address from the dropdown, populate the address
//    fields in the form. The unique parameter is to acomodate for autocomplete
//    and autocomplete2

function fillInAddress(autocomplete, unique) {
  // Get the place details from the autocomplete object.

  var place = autocomplete.getPlace();

  for (var component in componentForm) {
    if(!!document.getElementById(component + unique)) {
      document.getElementById(component + unique).value = '';
    // document.getElementById(component).disabled = false;
  }
}


  // Get each component of the address from the place details
  // and fill the corresponding hidden field on the form.
  for (var i = 0; i < place.address_components.length; i++) {
    var addressType = place.address_components[i].types[0];
    if (componentForm[addressType] && document.getElementById(addressType + unique)) {
      var val = place.address_components[i][componentForm[addressType]];
      document.getElementById(addressType + unique).value = val;
  }
  var searchstring = document.getElementById('autocomplete' + unique).value
  document.getElementById('searchstring' + unique).value = searchstring
  }

  // Add the lat/lng as hidden field to form
  if (place.geometry.location) {
      var lat = place.geometry.location.lat()
      document.getElementById('lat' + unique).value = lat;
      var lng = place.geometry.location.lng()
      document.getElementById('lng' + unique).value = lng;
  }

  // call AJAX function in search.js
  clearOffset();  
  newSearch();
}

// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate() {
          if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
              var geolocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
              };
              var circle = new google.maps.Circle({
                center: geolocation,
                radius: position.coords.accuracy
              });
              autocomplete.setBounds(circle.getBounds());
            });
          }
        }

function initAutocomplete() {
  // Create Autocomplete objects for start and finish
  autocomplete = new google.maps.places.Autocomplete(
      (document.getElementById('autocomplete')));

  autocomplete2 = new google.maps.places.Autocomplete(
      (document.getElementById('autocomplete2')));

  // Add event listeners to autocomplete objects
  autocomplete.addListener('place_changed', function() {
      fillInAddress(autocomplete, "");
  });
  
  autocomplete2.addListener('place_changed', function() {
      fillInAddress(autocomplete2, "2");
  });

}
