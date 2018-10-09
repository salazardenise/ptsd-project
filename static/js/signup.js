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
    //console.log("username entered " + username)
    $.get('/user_exists', {'username': username}, (result) => {
        //console.log("\n\n" + result + "\n\n")
        if (result == 'found') {
            //console.log('username taken')
            $('#signUpErrorMessage').html("Error: Username is already taken. Please enter a different one.")
            $('#signUpErrorMessage').show();
            setTimeout(() => $('#signUpErrorMessage').hide(), 5000)
        } else {
            //console.log('username not taken')
            // resubmit
            let form_data = {
                "first_name": $('#signUpFirstName').val(),
                "last_name": $('#signUpLastName').val(),
                "email": $('#signUpEmail').val(),
                "phone": $('#signUpPhone').val(),
                "username": $('#signUpUsername').val(),
                "password": $('#signUpPassword1').val()
            }
            $.post('/signup', form_data, () => { 
                //console.log('submit signup form')
                window.location.replace("/");
            });
        }
    });

});