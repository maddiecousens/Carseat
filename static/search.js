"use strict";

// $(function() {

    // Create seat # drop down, depending on how many seats left
    function htmlSeats(seats){
        var seatOptions;
        for (var i = 0; i < seats; i++) {

            seatOptions += ('<option value=' + (i+1) + '>' + (i+1)
                            + '</option> \
                                <span>');        }

        return seatOptions;
    }

    // Create HTML for every Data row
    function htmlRow(ride) {
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
                      <select class="form-control" name="seats" style="width:auto;">';
        
        row += htmlSeats(ride.seats);


        row += '<input type="hidden" name="ride_id" value="' + ride.ride_id
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
                      <span>';

            if (ride.start_name != null) {
                row += ride.start_name;
            }
            if (ride.start_number != null && ride.start_street != null) {
                row += ride.start_number + " " + ride.start_street + ", ";
            }
            if (ride.start_city != null) {
                row += ride.start_city + ", ";
            }
            if (ride.start_state != null) {
                if (ride.start_zip) {
                    row += ride.start_state + ", ";
                }
                else {
                    row += ride.start_state;
                }
            }
            if (ride.start_zip != null) {
                row += ride.start_zip;
            }

            row += '</span> \
                </p> \
              </div> \
              <div class="row"> \
                <p> \
                  <span class="glyphicon glyphicon-unchecked" style="color:red"></span> \
                  <span>'

            if (ride.end_name != null) {
                row += ride.end_name;
            }

            if (ride.end_number != null && ride.end_street != null) {
                row += ride.end_number + " " + ride.end_street + ", ";
            }
            if (ride.end_city != null) {
                row += ride.end_city + ", ";
            }
            if (ride.end_state != null) {
                if (ride.end_zip) {
                    row += ride.end_state + ", ";
                }
                else {
                    row += ride.end_state;
                }
            }
            if (ride.end_zip != null) {
                row += ride.end_zip;
            }

            row += '</span> \
                </p> \
              </div> \
            </td> \
            <td class="col-xs-2" style="padding-left:20px;"> \
              <div class="row"> \
                <span><h1>$'
                + ride.cost
                + '</h1></span> \
              </div> \
              <div class="row"> \
                <h4><small><i>per passenger</i><small></h4> \
                </div> \
                <div class="row"> \
                  <h4>'
                + ride.seats
                + ' Seats Left</h4> \
                </div> \
                <div class="row"> \
                  <a class="my-tool-tip" data-toggle="tooltip" \
                  data-placement="left" title="You are allowd to bring 1 '
                + ride.luggage
                + ' suitcase"> \
                   <span class="glyphicon glyphicon-heart col-xs-4" \
                   style="font-size:2em;"></span> \
                              </a>';

            if (ride.pickup_window === "flexible") {
                row += '<a class="my-tool-tip" data-toggle="tooltip" \
                data-placement="left" title="Pickup time is very flexible, \
                discuss with driver"> \
                <span class="glyphicon glyphicon-star col-xs-4" \
                style="font-size:2em;"></span> \
                  </a>';
            }
            else if (ride.pickup_window !== 'No') {
                row += '<a class="my-tool-tip" data-toggle="tooltip" \
                data-placement="left" title="Pickup time is flexible in a '
                + ride.pickup_window
                + ' window">=<span class="glyphicon glyphicon-star col-xs-4" \
                    style="font-size:2em;"></span> \
                  </a>';
            }

            if (ride.detour == "flexible") {
                row += '<a class="my-tool-tip" data-toggle="tooltip" \
                data-placement="left" title="Driver is very flexible with detours"> \
                <span class="glyphicon glyphicon-star-empty col-xs-4" style="font-size:2em;"> \
                </span> \
                  </a>';
            }
            else if (ride.detour !== 'No') {
                row += '<a class="my-tool-tip" data-toggle="tooltip" \
                data-placement="left" title="Driver is open to a '
                + ride.detour
                + ' detour"> \
                    <span class="glyphicon glyphicon-star-empty col-xs-4" style="font-size:2em;"></span> \
                  </a>';
            }

            row += '</div> \
                      </div> \
                    </td> \
                  </tr>';

        return row;
    }

    // Success Function to build html
    function buildHTML(data) {
        console.log(data);
        
        // Start building HTML
        var html = '<table class="table table-hover">';
        

        // For every ride in JSON, call htmlRow

        if (data.length > 0) {
            for (var i = 0; i < data.length; i++) {
                html += htmlRow(data[i]);
            }

            html += '</table></tbody>';

        }
        else {
            html += '<p>No upcoming rides for that search</p>';
        }

        $('#results').empty().append(html);
    }

    // Event Handler, AJAX
    function newSearch(evt) {

        // If user doesn't enter a from date, make it todays date
        var today = new Date()
        var today_string = (today.getMonth() 
                        + '/' 
                        + today.getDay() 
                        + '/' 
                        + today.getFullYear())

        if ($('#from').val()) {
            var date_from = $('#from').val()
        } else {
            var date_from = today_string
        }

      
        // Create data object to pass in AJAX call
        // console.log('start_lat:' + $('#lat').val(), 'end_lat:' + $('#lat2').val());
        
        var data = {start: $('.slider-time').val(),
                    cost: $('.slider-cost').val(),
                    start_state: $('#administrative_area_level_1').val(),
                    start_term: $('#searchstring').val(),
                    end_term: $('#searchstring2').val(),
                    start_lat: $('#lat').val(),
                    start_lng: $('#lng').val(),
                    end_lat: $('#lat2').val(),
                    end_lng: $('#lng2').val(),
                    date_from: date_from,
                    date_to: $('#to').val(),
                    user_lat: $('#user_lat').val(),
                    user_lng: $('#user_lng').val(),
                    limit: $('#dropdownMenu1').text().trim(),
                    offset: $('#current-offset').val()
        };
        console.log($('#current-offset').val());
        // console.log($('.slider-time').val());
        // console.log($('.slider-cost').val());
        // Ajax call
        $.get('/search-time.json', data, buildHTML);
    }


    

    // Reverse Button
    var reverseInput = function() {
        var old_auto2 = $('#autocomplete2').val();
        $('#autocomplete2').val($('#autocomplete').val());
        $('#autocomplete').val(old_auto2);

        var old_lat2 = $('#lat2').val();
        $('#lat2').val($('#lat').val());
        $('#lat').val(old_lat2);

        var old_lng2 = $('#lng2').val();
        $('#lng2').val($('#lng').val());
        $('#lng').val(old_lng2);

        var old_ss2 = $('#searchstring2').val();
        $('#searchstring2').val($('#searchstring').val());
        $('#searchstring').val(old_ss2);

        newSearch();
    }

    // Event Listeners for Toggles

    // Time and Cost Sliders
    $( '#slider-range-max' ).on( "slidechange", newSearch );
    $( '#slider-range-max-cost' ).on( "slidechange", newSearch );
    //To and From DATE changer
    $( '#to' ).on( "change", newSearch );
    $( '#from' ).on( "change", newSearch );
    // Reverse Button
    $('#reverse').on('click', reverseInput)


    


    // Click Event Listeners and Handlers for Pagination

    // Changing the results per page
    $('.dropdown-menu a').on('click', function(){    
        $('.dropdown-toggle').html($(this).html() + '<span class="caret"></span>');
        newSearch();    
    })

    // Page Numbers
    var pages = $('.page-number')
    // Initialize Page1 as the active class
    $('#page-number1').addClass('active')

    for (var i = 0; i < pages.length; i++) {
        pages[i].addEventListener('click', function(evt){

            var page = parseInt(evt.srcElement.childNodes[0].data);
            //Remove 'active' class from all page numbers
            $('.page-number').removeClass('active');
            // Add active class to Current Page
            $('#page-number' + page).addClass('active')
            // Subtracting 1 from page, because offset is 1 minus the page num
            $('#current-offset').val(page - 1);
            newSearch();
    });
    }

    // Previous button
    $('#previous').on('click', function(evt) {
        var current = parseInt($('#current-offset').val());

        if (current > 0) {
            // Subtract 1 from page offset if not already at 0
            $('#current-offset').val(current - 1);
            //Remove 'active' class from all page numbers
            $('.page-number').removeClass('active');
            //Add active class to Current Page (current offset bc when 
                //you go down a page, the previous page is the old offset)
            $('#page-number' + current).addClass('active')
            
            newSearch();
        }

    });

    // Next button
    $('#next').on('click', function(evt) {
        var current = parseInt($('#current-offset').val());
        var max = parseInt($('#max-offset').val());

        if (current < max) {
            // Add 1 from page offset if not already at 0
            $('#current-offset').val(current + 1);
            //Remove 'active' class from all page numbers
            $('.page-number').removeClass('active');
            //Add active class to Current Page (current +2 bc when 
                //you go up a page, the page is the old offset plus 2)
            $('#page-number' + (current + 2)).addClass('active');
            newSearch();
        }

    });
//to do: adjust hardcoded limit
