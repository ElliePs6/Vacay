$(document).ready(function() {
    // Date picker initialization for all elements with the 'datepicker' class
    $('.datepicker').datepicker();

    // Click event for the calendar icon buttons
    $('#start-calendar-icon, #end-calendar-icon').click(function() {
        $(this).prev('.datepicker').datepicker('show');
    });
});