document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');

    const calendar = new FullCalendar.Calendar(calendarEl, {
        locale: 'el', // Set Greek locale
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next,today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,list'
        },
        
        events: '/vacayvue/all_requests/',
        eventContent: function (arg) {
            return {
                html: `<div class="fc-list-item-title">${arg.event.title}</div>`
            };
        },
        // Function to adjust event rendering
        eventDidMount: function (arg) {
            
            // If the event spans multiple days
            if (arg.event.start !== arg.event.end) {
                // Adjust the event's end to show it until the end of the day
                const end = new Date(arg.event.end);
                end.setDate(end.getDate() + 1);
                arg.event.setEnd(end);
            }
        }
    });

    calendar.render();
})