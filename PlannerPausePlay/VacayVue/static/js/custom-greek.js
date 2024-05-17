// custom-greek.js

document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');

    const calendar = new FullCalendar.Calendar(calendarEl, {
        locale: 'el',
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next,today', // Removed space after commas
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,list'
        },
        events: '/vacayvue/all_requests/',
        buttonText: {
            today: 'Σήμερα',
            dayGridMonth: 'Μήνας',
            timeGridWeek: 'Εβδομάδα',
            list: 'Λίστα'
        }
    });

    calendar.render();

})


