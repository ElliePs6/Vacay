$(document).ready(function() {
    function showMessage(type, text) {
        var messageContainer = $('#message-container');
        var message = $('<div class="message"></div>');

        message.addClass(type);
        message.text(text);
        messageContainer.append(message);
        message.fadeIn();

        setTimeout(function() {
            message.fadeOut(function() {
                message.remove();
            });
        }, 3000); // Adjust the time as needed
    }
    
    $('.request-detail-link').click(function(e) {
        e.preventDefault();
        var requestId = $(this).data('request-id');
        var url = $(this).data('url');
        $.ajax({
            url: url,
            type: 'GET',
            async: true,
            data: {
                request_id: requestId
            },
            success: function(response) {
                $('#DetailModal .modal-content').html(response);
                $('#DetailModal').modal('show');
            },
            error: function(xhr, status, error) {
                showMessage('error', 'Σφάλμα κατά την ανάκτηση των λεπτομερειών του αιτήματος.');
            }
        });
    });

    $('.approve-btn').click(function() {
        var requestId = $(this).data('approve-request-id');
        $.ajax({
            url: `/vacayvue/approve_leave_request/${requestId}/`,
            type: 'GET',
            data: { action: 'approve' },  // Include the action parameter
            success: function(response) {
                if (response.success) {
                    showMessage('success', response.message);
                    setTimeout(function() {
                        location.reload();
                    }, 1000);
                } else {
                    showMessage('error', response.message);
                }
            },
            error: function(xhr, status, error) {
                showMessage('error', 'Παρουσιάστηκε σφάλμα κατά την επεξεργασία του αιτήματος');
            }
        });
    });

    $('.reject-btn').click(function(event) {
        event.preventDefault();
        var requestId = $(this).data('reject-request-id');
        $.ajax({
            url: `/vacayvue/reject_leave_request/${requestId}/`,
            type: 'GET',
            data: { action: 'reject' },  // Include the action parameter
            success: function(response) {
                if (response.success) {
                    showMessage('success', response.message);
                    setTimeout(function() {
                        location.reload();
                    }, 1000);
                } else {
                    showMessage('error', response.message);
                }
            },
            error: function(xhr, status, error) {
                showMessage('error', 'Παρουσιάστηκε σφάλμα κατά την επεξεργασία του αιτήματος.');
            }
        });
    });
});