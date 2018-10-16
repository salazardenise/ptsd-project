"use strict";

/* Set ip preview */
$('#bodyMessage').height($("#bodyMessage")[0].scrollHeight);

function updatePreviewMessage() {
    let fromFirstName = $('#fromFirstName').val();
    let fromLastName = $('#fromLastName').val();

    let toFirstName = $('#toFirstName').val();
    let toLastName = $('#toLastName').val();

    let bodyMessage = $('#bodyMessage').val();

    let contentMessage = 'Hi ' + toFirstName + ' ' + toLastName + ',<br><br>';
    contentMessage += bodyMessage + '<br><br>';
    contentMessage += 'Best,<br>' + fromFirstName + ' ' + fromLastName;

    $('#previewMessage').html(contentMessage)
}

/* catch changes to message */
$('#fromFirstName').on('keyup', () => {
    updatePreviewMessage();
});

$('#fromLastName').on('keyup', () => {
    updatePreviewMessage();
});

$('#toFirstName').on('keyup', () => {
    updatePreviewMessage();
});

$('#toLastName').on('keyup', () => {
    updatePreviewMessage();
});

$('#bodyMessage').on('keyup', () => {
    updatePreviewMessage();
});

/* user clicks to send text message*/
$('#sendTextMessageForm').on('submit', (evt) => {
    evt.preventDefault();
    console.log('coming up: validating the form')


});