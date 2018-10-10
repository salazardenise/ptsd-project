"use strict";

$('#signUpForm').on('submit', (evt) => {

    let password1 = $('#signUpPassword1').val();
    let password2 = $('#signUpPassword2').val();

    if (password1 != password2) {
        evt.preventDefault();
        $('#signUpErrorMessage').html("Error: Re-entered password does not match password. Please check this.")
        $('#signUpErrorMessage').show();
        setTimeout(() => $('#signUpErrorMessage').hide(), 5000)
        return;
    }

    evt.preventDefault();

    let username = $('#signUpUsername').val()
    $.get('/user_exists', {'username': username}, (result) => {
        if (result == 'found') {
            $('#signUpErrorMessage').html("Error: Username is already taken. Please enter a different one.")
            $('#signUpErrorMessage').show();
            setTimeout(() => $('#signUpErrorMessage').hide(), 5000)
        } else {
            // resubmit form 
            $('#signUpForm').unbind('submit').submit();
        }
    });

});