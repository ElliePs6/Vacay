document.addEventListener("DOMContentLoaded", function() {
    // Retrieve the requestId from the URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const requestId = urlParams.get('requestId');

    // Fetch the request details using AJAX or other methods
    // Populate the form fields with the details of the current request
    // Example:
    fetch(`vacayvue/get_request_details/${requestId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('type').value = data.type;
            document.getElementById('description').value = data.description;
            document.getElementById('start').value = data.start;
            document.getElementById('end').value = data.end;
        })
        .catch(error => {
            console.error('Error fetching request details:', error);
            alert('An error occurred while fetching request details');
        });

    // Handle form submission
    document.getElementById('edit-request-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        // Submit form data via AJAX or other methods to update the request
        fetch(`vacayvue/update_request/${requestId}`, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Request updated successfully');
                // Redirect back to the calendar page or another page
                window.location.href = 'vacayvue/request_calendar.html';
            } else {
                alert('Failed to update request');
            }
        })
        .catch(error => {
            console.error('Error updating request:', error);
            alert('An error occurred while updating request');
        });
    });
});
