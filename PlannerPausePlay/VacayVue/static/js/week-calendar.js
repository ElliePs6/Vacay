document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar2');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        themeSystem: 'bootstrap5',
        locale: 'el',
        initialView: 'dayGridWeek',
        events: '/vacayvue/all_requests/',
        
        // Remove slotLabelInterval option to hide hourly slots
        // Other configurations...
    });

    calendar.render();
});
