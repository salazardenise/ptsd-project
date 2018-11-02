"use strict";

$('#editPasswordForm').on('submit', (evt) => {

    let current_password = $('#userProfileCurrentPassword').val();
    let new_password1 = $('#userProfilePassword1').val();
    let new_password2 = $('#userProfilePassword2').val();

    if (new_password1 != new_password2) {
        evt.preventDefault();
        $('#userProfileErrorMessage').html("Error: New re-entered password does not match new password. Please check this.")
        $('#userProfileErrorMessage').fadeIn(400, () => {
            setTimeout(() => {$('#userProfileErrorMessage').fadeOut(400,)}, 5000);
        });
        return;
    }

    evt.preventDefault();

    $.post('/change_password', 
          {'current_password': current_password, 'new_password1': new_password1},
          (result) => {
            console.log('THE RESULT');
            console.log(result);
            if (result.valid_password_change == true) {
                // valid_password_change was true and done, redirect to home
                window.location.href = '/';
            }
            else {
                $('#userProfileErrorMessage').html("Error: Current password is not correct. Please check this.")
                $('#userProfileErrorMessage').fadeIn(400, () => {
                    setTimeout(() => {$('#userProfileErrorMessage').fadeOut(400,)}, 5000);
                });
            }
    });

});