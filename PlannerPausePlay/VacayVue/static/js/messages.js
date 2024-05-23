$(document).ready(function() {
    // Function to display error message
    function showErrorMessage(message) {
        var errorContainer = $('#error-container');
        var errorMessage = $('<div class="message error"></div>');
        errorMessage.text(message);
        errorContainer.append(errorMessage);
    }

    // Check if there is an error message in the context
    var error_message = "{{ error_message }}"; // Get the error message from the context
    if (error_message) {
        showErrorMessage(error_message);
    }
});
