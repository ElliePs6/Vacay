$(document).ready(function() {
    // Date picker initialization for all elements with the 'datepicker' class
    $('.datepicker').datepicker({
        format: 'dd/mm/yy',  // Set the desired date format
        autoclose: true,
        todayHighlight: true,
        clearBtn: true,
        // Any other options you want to include
    });

    // Click event for the calendar icon buttons
    $('#start-calendar-icon, #end-calendar-icon').click(function() {
        $(this).prev('.datepicker').datepicker('show');
    });
});