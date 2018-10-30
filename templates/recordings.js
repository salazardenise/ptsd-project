$('.recording-star').on('click', (evt) => {
    let recordingStar = $(evt.target)
    let recording_id = recordingStar.data('recordingid')
    $.get('/toggle_favorite_recording', {'recording_id': recording_id}, (results) => {
        if (results.user_logged_in == true) {
            // A user is logged in
            if (results.favorite == true) {
                // user favorited the recording, toggle star to solid
                recordingStar.removeClass('far').addClass('fas');
            } else {
                // user unfavorited the recording, toggle star to regular
                recordingStar.removeClass('fas').addClass('far');
            }
        } else {
            // A user is not logged in, show error message
            $('#recordingsErrorMessage').fadeIn(400, () => {
                setTimeout(() => {$('#recordingsErrorMessage').fadeOut(400,)}, 5000);
            });
        }
    });
});