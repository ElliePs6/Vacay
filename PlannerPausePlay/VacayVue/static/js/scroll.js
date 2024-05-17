document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.fc-list-item-title').forEach(function(element) {
        element.addEventListener('click', function(event) {
            const delta = this.classList.contains('before') ? -1 : 1; // Determine scroll direction
            this.scrollLeft += delta * 20; // Adjust scroll speed as needed
        });
    });
});
