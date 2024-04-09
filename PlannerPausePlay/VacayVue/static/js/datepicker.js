$(document).ready(function() {
    $('.datepicker').datepicker({ // Date picker initialization 
        dateFormat: 'YYYY-MM-DD'  
    });

    // Click event for the calendar icon buttons
    $('#join_date').click(function() {
        $(this).prev('.datepicker').datepicker('show');
    });
});

/** 
{
    format: 'dd/mm/yy',  // Set the desired date format
    autoclose: true,
    todayHighlight: true,
    clearBtn: true,
    // Any other options you want to include
}*/