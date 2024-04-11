document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
		    headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,list'
        },
        selectable: true,
        editable: true,
        slotDuration: '00:04:00',
        //weekend:false,
       // hiddenDays: [0, 6],
        events: "/vacayvue/all_requests/",
        select: function(info) {
            console.log("Selecting dates...");
            $('#requestModal').modal('show');
            $('#id_start').val(info.startStr);
            $('#id_end').val(info.endStr);
          //  $('#requestModal').modal('hide');
        },
        eventClick: function(info) {
            console.log("Clicked request:", info.event);
            var event = info.event;
            var modal = $('#detailModal');
            modal.find('#type_request_detail').text(event.extendedProps.type);
            modal.find('#start_request_detail').text(event.startStr);
            modal.find('#end_request_detail').text(event.endStr);
            modal.find('#description_request_detail').text(event.extendedProps.description || '');
            modal.find('#delete-request-button').attr('data-request-id', event.id);
            modal.modal('show');
			$('#requestModal').modal('hide');
        },

		
		});
    calendar.render();

    // Event listeners using event delegation
    $(document).on('click', '.modalClose', handleCloseModal);
    $(document).on('click', '.submitRequestForm', handleSubmitRequestForm);
   
  
    function handleCloseModal() {
        console.log("Closing modal...");
        $(this).closest('.modal').modal('hide');
    }

    function handleSubmitRequestForm() {
        console.log("Submitting request form...");
        var formData = $(this).closest('form').serialize();
        $.ajax({
            url: "/vacayvue/add_request/",//for static urls
            type: 'POST',
            data: formData,
            dataType: 'json',
            success: function (response) {
                console.log("Form submission response:", response);
                if (response.success) {
                    $('#requestModal').modal('hide');
                    window.location.reload();
                } else {
                    console.log(response.errors);
                }
            },
            error: function (xhr, status, error) {
                console.error("Error submitting form:", xhr.responseText);
                if (xhr.status === 404) {
                    alert('The request does not exist.');
                } else {
                    alert('There was an error processing your request.');
                }
            }
        });
    }


    document.getElementById('delete-request-button').addEventListener('click', function() {
        const requestId = this.getAttribute('data-request-id');
        console.log("Request ID:", requestId);
        if (confirm('Are you sure you want to delete this event?')) {
            $.ajax({
                url: `/vacayvue/delete_request/${requestId}/`,//For dynamic urls
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(response) {
                    alert(response.message);
                    window.location.reload();
                },
                error: function(xhr, status, error) {
                    alert('Error!');
                }
            
            });
        }});
        
        
        
});
