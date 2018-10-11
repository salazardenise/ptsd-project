"use strict";

$('#logInForm').on('submit', (evt) => {
    evt.preventDefault();

    let password = $('#logInPassword').val();
    let username = $('#logInUsername').val();

    $.post('/validate_login', {'username': username, 'password': password}, (result) => {
        if (result.username_found == false) { // username does not exist
            $('#logInErrorMessage').html("Error: Username not recognized.")
            $('#logInErrorMessage').fadeIn(400, () => {
                setTimeout(() => {$('#logInErrorMessage').fadeOut(400,)}, 5000);
            });
        }
        else { // username exists
            if (result.valid_login == false) { // username and password do not match
                $('#logInErrorMessage').html("Error: Username and password do not match")
                $('#logInErrorMessage').fadeIn(400, () => {
                    setTimeout(() => {$('#logInErrorMessage').fadeOut(400,)}, 5000);
                });
            }
            else {
                // login is valid, resubmit form
                $('#logInForm').unbind('submit').submit();
            }
        }
    });

    // $.get('/user_exists', {'username': username}, (result) => {
    //     if (result != 'found') {
    //         $('#logInErrorMessage').html("Error: Username not recognized.")
    //         $('#logInErrorMessage').fadeIn(400, () => {
    //             setTimeout(() => {$('#logInErrorMessage').fadeOut(400,)}, 5000);
    //         });
    //     } 
    //     else {
    //         $.post('/validate_login', 
    //               {'username': username, 'password': password},
    //               (result) => {
    //                     if (result != 'valid') {
    //                         $('#logInErrorMessage').html("Error: Username and password do not match")
    //                         $('#logInErrorMessage').fadeIn(400, () => {
    //                             setTimeout(() => {$('#logInErrorMessage').fadeOut(400,)}, 5000);
    //                         });
    //                     } else {
    //                         // resubmit form
    //                         $('#logInForm').unbind('submit').submit();
    //                     }
    //               });
    //     }
    // });
});