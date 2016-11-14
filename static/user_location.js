var options = {
  enableHighAccuracy: true,
  timeout: 5000,
  maximumAge: 0
};

function success(pos) {
  var crd = pos.coords;

  $('#user_lat').val(crd.latitude);
  $('#user_lng').val(crd.longitude);
  // console.log($('#user_lat').val());
  // console.log($('#user_lng').val());

};

function error(err) {
  console.log('ERROR(' + err.code + '): ' + err.message);
};

navigator.geolocation.getCurrentPosition(success, error, options);
