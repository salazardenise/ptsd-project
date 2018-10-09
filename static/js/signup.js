"use strict";

$('#signUpForm').on('submit', (evt) => {
    
    let password1 = $('#signUpPassword1').val();
    let password2 = $('#signUpPassword2').val();

    if (password1 != password2) {
        evt.preventDefault();
        $('#signUpErrorMessage').show();
        setTimeout(() => $('#signUpErrorMessage').hide(), 3000)
    }

});