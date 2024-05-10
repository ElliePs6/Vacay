$(function() {
    $.datepicker.setDefaults($.datepicker.regional['el']);

    $("#id_join_date").datepicker({
        dateFormat: "dd/mm/yy", // Display format
        altFormat: "dd-mm-yy",  // Format expected by Django
        altField: "#id_join_date", // Hidden field for Django
    });
    $("#id_start").datepicker({
        dateFormat: "dd/mm/yy", 
        altFormat: "yy-mm-dd",  
        altField: "#id_start", 
    });

    $("#id_end").datepicker({
        dateFormat: "dd/mm/yy", 
        altFormat: "yy-mm-dd",  
        altField: "#id_end", 
    });
});