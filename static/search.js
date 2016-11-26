"use strict";

var rides, pageCount;

    function pagination(pageCount) {
        var paginationHTML = '<nav aria-label="Page navigation"> \
            <ul class="pagination"> \
              <li id="previous"> \
                <a href="#" aria-label="Previous"> \
                  <span aria-hidden="true">&laquo;</span> \
                </a> \
              </li>';
        for (var i = 0; i < pageCount; i++) {
            paginationHTML += '<li class="page-number" data-pagenumber="'
            + (i + 1)
            + '" id="page-number'
            + (i + 1)
            + '"><a href="#">'
            + (i + 1)
            + '</a></li>';

        };

        paginationHTML += '<li id="next"> \
                          <a href="#" aria-label="Next"> \
                            <span aria-hidden="true">&raquo;</span> \
                          </a> \
                          </li> \
                        </ul> \
                      </nav>\
                      </div>';
        // console.log(paginationHTML);
        $('#pagination').empty().append(paginationHTML);

    }

    // Create seat # drop down, depending on how many seats left
    function htmlSeats(seats){
        var seatOptions;
        for (var i = 0; i < seats; i++) {

            seatOptions += ('<option value=' + (i+1) + '>' + (i+1)
                            + '</option>');        
        }

        return seatOptions;
    }

    // Create HTML for every Data row
    function htmlRow(ride) {
        var row = '<tr> \
            <td class="col-xs-2" id="left-data"> \
                <div class="row"> \
                <img class="img-responsive" src="'
            + ride.user_image
            + '" alt="driver image" width="100" height="100"> \
              </div> \
              <div class="row"> \
                <div>'
            + ride.user_first_name
            + '</div> \
                <div> \
                  <form action="/request-seats" method="POST"> \
                    <div class="input-group"> \
                      <select class="form-control" id="seats" name="seats">';
        
        row += htmlSeats(ride.seats);

        row += '</select> \
                <span> \
                  <input type="hidden" name="ride_id" value="' 
            + ride.ride_id
                + '"><input class="btn btn-custom request-seats" type="submit" value="Request Seats"></span> \
                </div> \
                      </form> \
                    </div> \
                  </div> \
                </td> \
                <td class="col-xs-8" id="middle-data"> \
                  <div class="row ride" '
                + 'data-startlat="'
                + ride.start_lat
                + '" data-startlng="'
                + ride.start_lng
                + '" data-endlat="'
                + ride.end_lat
                + '" data-endlng="'
                + ride.end_lng
                +'"> \
                  <div class="departure-date light-gray">'
                + ride.start_timestamp
                + '</div> \
                   </div> \
                  <div class="row cities"> \
                    <div>'
                + ride.start_city
                + ', '
                + ride.start_state
                + ' <span class="arrow-ie">→</span> '
                + ride.end_city
                + ', '
                + ride.end_state
                + '</div> \
                    </div> \
                    <br> \
                  <div class="row"> \
                    <div class="specific-address"> \
                        <span class="glyphicon start glyphicon-unchecked"></span> \
                        <span class="pickup-dropoff">Pick-up: </span> \
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
              </div> \
              </div> \
              <div class="row"> \
                <div class="specific-address"> \
                  <span class="glyphicon end glyphicon-unchecked"></span> \
                  <span class="pickup-dropoff">Drop-off: </span> \
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
                </div> \
              </div> \
              <br>'
            if (ride.mileage != null & ride.duration != null) {
                row += '<span class="glyphicon glyphicon-time"></span> \
                <span>'
                + ride.mileage
                + ', Est Travel Time: '
                + ride.duration
                + '</span>'
            }
            row += '<div class="row"> \
            <button type="button"class="btn btn-link view-route-btn">View Route <span class="glyphicon glyphicon-chevron-down"></span></button> \
              </div> \
              <div class="add-map-here"></div> \
          </td> \
            <td class="col-xs-2" id="right-data"> \
            <div class="row"> \
              <span class="price">$'
                + ride.cost
                + '</span> \
              <span class="per-passenger">per passenger</span> \
            </div> \
            <div class="row"> \
              <span class="seats-left">'
                + ride.seats
                + '<span> \
              <span class="seats-left-number">seats left</span> \
            </div> \
            <br><br><br> \
                <div class="row pull-right"> \
              <a class="my-tool-tip" data-toggle="tooltip" data-placement="left" title="You are allowd to bring 1 '
                + ride.luggage
                + ' suitcase"> \
                   <i class="icon-briefcase icon-large col-xs-4"></i> \
                    </a>';

            if (ride.pickup_window === "flexible") {
                row += '<a class="my-tool-tip" data-toggle="tooltip" data-placement="left" title="Pickup time is very flexible, discuss with driver"> \
                <i class="icon-time icon-large col-xs-4"></i> \
              </a>';
            }
            else if (ride.pickup_window !== 'No') {
                row += '<a class="my-tool-tip" data-toggle="tooltip" \
                data-placement="left" title="Pickup time is flexible in a '
                + ride.pickup_window
                + ' window"> \
                    <i class="icon-time icon-large col-xs-4"></i> \
                    </a>';
            }

            if (ride.detour == "flexible") {
                row += '<a class="my-tool-tip" data-toggle="tooltip" data-placement="left" title="Driver is very flexible with detours"> \
                <i class="icon-undo icon-large col-xs-4"></i> \
              </a>';
            }
            else if (ride.detour !== 'No') {
                row += '<a class="my-tool-tip" data-toggle="tooltip" \
                data-placement="left" title="Driver is open to a '
                + ride.detour
                + ' detour"> \
                    <i class="icon-undo icon-large col-xs-4"></i> \
                    </a>';
            }

            row += '</div> \
                   </td> \
                  </tr>';

        return row;
    }

$(document).ajaxSuccess(function() {
        var activePage = parseInt($('#current-offset').val()) + 1
        $('#page-number' + activePage).addClass('active')
});


    // Success Function to build html
    function buildHTML(data) {
        pageCount = data[0].page_count;
        console.log('pageCount: ' + pageCount);
        rides = data[1];
        console.log(rides);

        // Replace Pagination
        // var limit = $('#dropdownMenu1').text().trim()
        pagination(pageCount);
        $('#max-offset').val(pageCount - 1);
        
        // Start building HTML
        var html = '<table class="table table-hover" id="results"> \
                        <tbody>';
        

        // For every ride in JSON, call htmlRow

        if (rides.length > 0) {
            for (var i = 0; i < rides.length; i++) {
                html += htmlRow(rides[i]);
            }

            html += '</table></tbody>';

        }
        else {
            html += '<tr> \
                      <td> \
                        <p>No upcoming rides for that search</p> \
                      </td> \
                    </tr>';
        }

        $('#results').empty().append(html);
        $('.view-route-btn').on("click", initMap);
    }

    // Event Handler, AJAX
    function newSearch(evt) {

        // If user doesn't enter a from date, make it todays date
        var today = new Date()
        var today_string = (today.getMonth() 
                        + '/' 
                        + today.getDate() 
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
                    offset: $('#current-offset').val(),
                    order: $('#active-orderby-btn').data('orderby')
        };
        console.log('data to backend:');
        console.log(data);
        console.log('current-offset: ' + $('#current-offset').val());

        // Ajax call
        $.get('/search.json', data, buildHTML);
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


    $('body').on('click', '.page-number', function(evt) {
            var page = $(this).data('pagenumber')

            // Subtracting 1 from page, because offset is 1 minus the page num
            $('#current-offset').val(page - 1);
            newSearch();
    });

    // Previous button
    $('body').on('click', '#previous', function(evt) {

        var current = parseInt($('#current-offset').val());

        if (current > 0) {
            // Subtract 1 from page offset if not already at 0
            $('#current-offset').val(current - 1);
            newSearch();
        }

    });

    // Next button
    $('body').on('click', '#next',  function(evt) {
        var current = parseInt($('#current-offset').val());
        var max = parseInt($('#max-offset').val());

        if (current < max) {
            // Add 1 from page offset if not already at 0
            $('#current-offset').val(current + 1);
            newSearch();
        }

    });

    // Order By Buttons
    function orderBy(evt) {
        //Remove 'active-orderby-btn' id from all buttons
        $('.orderbybtn').removeAttr('id','active-orderby-btn');
        // Add active-orderby-btn id to selection
        $(this).attr('id','active-orderby-btn');
        console.log($('#active-orderby-btn').data('orderby'));

        $('#current-offset').val(0); 
        newSearch();

        

    }

    $('.orderbybtn').on('click', orderBy)
//to do: adjust hardcoded limit
