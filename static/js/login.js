"use strict";

$('#logInForm').on('submit', (evt) => {
    evt.preventDefault();

    let password = $('#logInPassword').val();
    let username = $('#logInUsername').val();

    $.get('/user_exists', {'username': username}, (result) => {
        if (result != 'found') {
            $('#logInErrorMessage').html("Error: Username not recognized.")
            $('#logInErrorMessage').fadeIn(400, () => {
                setTimeout(() => {$('#logInErrorMessage').fadeOut(400,)}, 5000);
            });
        } 
        else {
            $.post('/validate_login', 
                  {'username': username, 'password': password},
                  (result) => {
                        if (result != 'valid') {
                            $('#logInErrorMessage').html("Error: Username and password do not match")
                            $('#logInErrorMessage').fadeIn(400, () => {
                                setTimeout(() => {$('#logInErrorMessage').fadeOut(400,)}, 5000);
                            });
                        } else {
                            // resubmit form
                            $('#logInForm').unbind('submit').submit();
                        }
                  });
        }
    });
});