$('.message-description').on('click', (evt) => {
    descriptionBox = $(evt.target);
    if (descriptionBox.hasClass('message-description')) {
        descriptionBox.removeClass('message-description');
    } else {
        descriptionBox.addClass('message-description');
    }
})

$('.message-star').on('click', (evt) => {
    messageStar = $(evt.target)
    message_id = messageStar.data('messageid')
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