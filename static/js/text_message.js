"use strict";

function updatePreviewMessage() {

    let toName = $('#toName').val();
    let bodyMessage = $('#bodyMessage').val();

    let fromFirstName = $('#fromFirstName').val()
    let fromLastName = $('#fromLastName').val()

    let contentMessage = 'Hi ' + toName + ',<br><br>';
    contentMessage += bodyMessage + '<br><br>';
    contentMessage += 'Best,<br>' + fromFirstName + ' ' + fromLastName;

    $('#previewMessage').html(contentMessage)
}

/* catch changes to message */
$('#toName').on('keyup', () => {
    updatePreviewMessage();
});

$('#bodyMessage').on('keyup', () => {
    updatePreviewMessage();
});