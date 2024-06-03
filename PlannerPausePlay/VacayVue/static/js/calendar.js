document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');

    const calendar = new FullCalendar.Calendar(calendarEl, {
        googleCalendarApiKey: 'AIzaSyAadAkcwKCpmMhWOLrjRbh_rkGRO6a0ePc', // Replace with your API key
        eventSources: [
            {
                googleCalendarId: 'el.greek.official#holiday@group.v.calendar.google.com',
                className: 'greek-holiday'
            },
            {
                googleCalendarId: 'el.islamic#holiday@group.v.calendar.google.com',
                className: 'islamic-holiday'
            },
            
        ],
        themeSystem: 'bootstrap5',
        locale: 'el', // Set Greek locale
        initialView: 'dayGridMonth',
        height: '100%',
        headerToolbar: {
            left: 'prev,next,today',
            center: 'title',
            right: 'dayGridMonth,dayGridWeek,list'
        },
        dayMaxEvents: true,
        expandRows: true,
        events:'/vacayvue/all_requests/',
        eventContent: function (arg) {
            return {
                html: `<div class="fc-list-item-title">${arg.event.title}</div>`,
                display: 'block', // Ensure each event is displayed as a block element
                'max-height': '30px', // Set the maximum height for each event
                overflow: 'hidden' // Hide overflow content if event content exceeds the maximum height
            };
        },
        eventDidMount: function (arg) {
            if (arg.event.start !== arg.event.end) {
                const end = new Date(arg.event.end);
                end.setDate(end.getDate() + 1);
                arg.event.setEnd(end);
            }
        }
    });

    calendar.render();
});
