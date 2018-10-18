"use strict";

/* Set ip preview */
$('#bodyMessageEmail').height($("#bodyMessageEmail")[0].scrollHeight);

function updatePreviewMessage() {

    let toName = $('#toNameEmail').val();
    let bodyMessage = $('#bodyMessageEmail').val();

    let fromFirstName = $('#fromFirstNameEmail').val()
    let fromLastName = $('#fromLastNameEmail').val()

    let contentMessage = 'Dear ' + toName + ',<br><br>';
    contentMessage += bodyMessage + '<br><br>';
    contentMessage += 'Best,<br>' + fromFirstName + ' ' + fromLastName;

    $('#previewMessage').html(contentMessage)
}

/* catch changes to message */
$('#toNameEmail').on('keyup', () => {
    updatePreviewMessage();
});

$('#bodyMessageEmail').on('keyup', () => {
    updatePreviewMessage();
});