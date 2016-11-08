$(function() {


function htmlSeats(seats){
    console.log('got into htmlSeats')
    var seatOptions;
    for (i = 0; i < seats; i++) {
        console.log('htmlSeats i' + i)

        seatOptions += ('<option value=' + (i+1) + '>' + (i+1)
                        + '</option> \
                            <span>')
        console.log(seatOptions);
    }

    return seatOptions;
}


function htmlRow(ride){
    console.log('inside htmlRow');
    var row = '<tbody> \
      <tr> \
        <td class="col-xs-2" style="padding-right:20px; border-right: 1px \
        solid #ccc;"> \
          <div class="row"> \
            <img class="img-responsive" src="'
        + ride.user_image
        + '" alt="driver image" width="100" height="100"> \
          </div> \
          <div class="row"> \
            <div> \
              <h5>'
        + ride.user_first_name
        + '</h5> \
            </div> \
            <div> \
              <form action="/request-seats" method="POST"> \
                <div class="input-group"> \
                  <select class="form-control" name="seats" style="width:auto;">'

    row += htmlSeats(ride.seats);

    row = row + '<input type="hidden" name="ride_id" value="' + ride.ride_id
            + '"></input><input class="btn btn-default" type="submit" value="Request Seats"></span> \
            </div> \
                  </form> \
                </div> \
              </div> \
            </td> \
            <td class="col-xs-8" style="padding-right:20px; padding-left:20px; border-right: 1px solid #ccc;"> \
              <div class="row"> \
                <h4>'
            + ride.start_timestamp
            + '</h4> \
                </div> \
              <div class="row"> \
                <h5>'
            + ride.start_city
            + ', '
            + ride.start_state
            + ' <span class="glyphicon glyphicon-arrow-right"></span> '
            + ride.end_city
            + ', '
            + ride.end_state
            + '</h5> \
               </div> \
              <div class="row"> \
                <p> \
                  <span class="glyphicon glyphicon-unchecked" style="color:green"></span> \
                  <span>'
        // if (ride.start_name != null) {

        // }

    return row;

}

    // Function to build html
    function buildHTML(data) {
        console.log(data);
        console.log(data.length);
        
        // Start building html
        var html = '<table class="table table-hover">';
        console.log(html);

        // For every ride in JSON, call htmlRow
        for (i = 0; i < data.length; i++) {
            console.log('buildHtml i ' + i);

            html += htmlRow(data[i]);
        }
        console.log(html);
    }


    // Event Handler, AJAX
    function newSearch(evt) {
      $.get('/jsontest.json', buildHTML);
    }

    // Event Listener on toggle
    $('.ui-slider-handle').on('mouseup', newSearch);


  });