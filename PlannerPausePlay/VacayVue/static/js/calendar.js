document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');

    const calendar = new FullCalendar.Calendar(calendarEl, {
        locale: 'el',
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next,today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,list'
        },
        
        events: '/vacayvue/all_requests/' ,
        eventContent: function (arg) {
            return {
                html: `<div class="fc-list-item-title">${arg.event.title}</div>`
            };
        } 
        
    });

    calendar.render();
})