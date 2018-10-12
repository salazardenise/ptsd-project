$('.message-description').on('click', (evt) => {
    descriptionBox = $(evt.target);
    if (descriptionBox.hasClass('message-description')) {
        descriptionBox.removeClass('message-description');
    } else {
        descriptionBox.addClass('message-description');
    }
})