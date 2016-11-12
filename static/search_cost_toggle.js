$( function() {

    $( "#slider-range-max-cost" ).slider({

      // Calculaions from  @JeffWeinberg http://jsfiddle.net/jrweinb/MQ6VT/
      range: "max",
      min: 0,
      max: 50,
      step: 1,
      value: 50,
      slide: function( event, ui ) {
        
        $('.slider-cost').html('$' + ui.value);
        $('.slider-cost').val(ui.value);
      }
    });
    $('.slider-cost').html('$50');
    $('.slider-cost').val( "50" );

  } );