function initializeCalendar() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        selectable: true,
        editable: true,
        events: "/vacayvue/all_requests/",
        select: function(info) {
            console.log("Selecting dates...");
            $('#requestModal').modal('show');
            $('#id_start').val(info.startStr);
            $('#id_end').val(info.endStr);
            calendar.unselect(); // Instead of calendar.fullCalendar('unselect')
        }
    });
    calendar.render();

    // Remove the event listener after execution
    document.removeEventListener('DOMContentLoaded', initializeCalendar);
}

document.addEventListener('DOMContentLoaded', initializeCalendar);
