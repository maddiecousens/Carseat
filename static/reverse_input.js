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
}

$('#reverse').on('click', reverseInput)