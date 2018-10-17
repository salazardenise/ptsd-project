$('.message-description').on('click', (evt) => {
    descriptionBox = $(evt.target);
    if (descriptionBox.hasClass('message-description')) {
        descriptionBox.removeClass('message-description');
    } else {
        descriptionBox.addClass('message-description');
    }
})

$('.message-star').on('click', (evt) => {
    messageStar = $(evt.target);
    message_id = messageStar.data('messageid');
    $.get('/toggle_favorite_message', {'message_id': message_id}, (results) => {
        if (results.user_logged_in == true) {
            // A user is logged in
            if (results.favorite == true) {
                // user favorited the message, toggle star to solid
                messageStar.removeClass('far').addClass('fas');
            } else {
                // user unfavorited the recording, toggle star to regular
                messageStar.removeClass('fas').addClass('far');
            }
        } else {
            // A user is not logged in, show error message
            $('#messagesErrorMessage').fadeIn(400, () => {
                setTimeout(() => {$('#messagesErrorMessage').fadeOut(400,)}, 5000);
            });
        }
    });
});

$('.text-button').on('click', (evt) => {
    textButton = $(evt.target);
    message_id = textButton.data('messageid');
    $.get('/validate_logged_in', (results) => {
        if (results.user_logged_in == true) {
            // A user is logged in, redirect to text_message page
            window.location.href = '/text_message?message_id=' + message_id;
        } else {
            // A user is not logged in, show error message
            $('#textMessageErrorMessage').fadeIn(400, () => {
                setTimeout(() => {$('#textMessageErrorMessage').fadeOut(400,)}, 5000);
            });
        }
    });
});

$('.email-button').on('click', (evt) => {
    textButton = $(evt.target);
    message_id = textButton.data('messageid');
    $.get('/validate_logged_in_with_gmail', (results) => {
        if (results.user_logged_in == true) {
            // A user is logged in, check if they have a gmail email address
            if (results.has_gmail == true) {
            // redirect to email_message page
            window.location.href = '/email_message?message_id=' + message_id;
            } else {
                $('#gmailMessageErrorMessage').fadeIn(400, () => {
                setTimeout(() => {$('#gmailMessageErrorMessage').fadeOut(400,)}, 5000);
            });
            }
        } else {
            // A user is not logged in, show error message
            $('#emailMessageErrorMessage').fadeIn(400, () => {
                setTimeout(() => {$('#emailMessageErrorMessage').fadeOut(400,)}, 5000);
            });
        }
    });
});