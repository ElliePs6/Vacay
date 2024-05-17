
$(function() {
    $.datepicker.setDefaults($.datepicker.regional['el']);

    $("#id_join_date").datepicker({
        dateFormat: "dd/mm/yy", // Display format
        altFormat: "yy-mm-dd",  // Format expected by Django
        altField: "#id_join_date", // Hidden field for Django
        onSelect: function(dateText, inst) {
            var date = $.datepicker.parseDate("dd/mm/yy", dateText);
            $("#id_join_date").val($.datepicker.formatDate("dd/mm/yy", date));
        }
    });
    $("#id_start").datepicker({
        dateFormat: "dd/mm/yy", // Display format
        altFormat: "yy-mm-dd",  // Format expected by Django
        altField: "#id_start", // Hidden field for Django
        onSelect: function(dateText, inst) {
            var date = $.datepicker.parseDate("dd/mm/yy", dateText);
            $("#id_start").val($.datepicker.formatDate("dd/mm/yy", date));
        }
    });
    
    $("#id_end").datepicker({
        dateFormat: "dd/mm/yy", // Display format
        altFormat: "yy-mm-dd",  // Format expected by Django
        altField: "#id_end", // Hidden field for Django
        onSelect: function(dateText, inst) {
            var date = $.datepicker.parseDate("dd/mm/yy", dateText);
            $("#id_end").val($.datepicker.formatDate("dd/mm/yy", date));
        }
    });
    

});