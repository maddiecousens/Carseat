var request = $('.request-seats')

function promptLogin(data) {
    console.log(data)
    if (data['logged_in'] != true) {
        console.log('log in yo')
        return
    }
    else {
        $('#request-seats').submit()
        console.log("yo submit the form")

    }
}

function requestSeats(evt) {
    evt.preventDefault();
    $.get('/check-login.json', promptLogin);
    evt.stopPropagation();
    $('#login').addClass('open')
    $('html, body').animate({ scrollTop: 0 }, 'fast');
    $('#status').text('Please log in to request a ride');
    
};

$('body').on('click', '.request-seats', requestSeats);


function preventSubmit(evt) {
    evt.preventDefault();
  }

$('#searchform').on("submit", preventSubmit);

$("a.my-tool-tip").tooltip();