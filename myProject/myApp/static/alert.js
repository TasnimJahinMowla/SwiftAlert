// Create a JavaScript function to display alert messages.
function showAlert(message, alertType) {
    var alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-' + alertType + ' alert-dismissible fade show';

    var closeButton = document.createElement('button');
    closeButton.type = 'button';
    closeButton.className = 'btn-close';
    closeButton.setAttribute('data-bs-dismiss', 'alert');
    closeButton.setAttribute('aria-label', 'Close');

    var alertText = document.createElement('strong');
    alertText.textContent = 'Alert: ';

    var messageText = document.createTextNode(message);
    alertText.appendChild(messageText);

    alertDiv.appendChild(alertText);
    alertDiv.appendChild(closeButton);

    var alertContainer = document.getElementById('alert-messages');
    alertContainer.appendChild(alertDiv);

    // Automatically remove the alert after a few seconds (e.g., 5 seconds).
    setTimeout(function() {
        alertContainer.removeChild(alertDiv);
    }, 5000); // 5000 milliseconds = 5 seconds
}
