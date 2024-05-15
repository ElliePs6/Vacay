$(document).ready(function() {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');

    // Add event listener to each checkbox
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('click', function() {
            // Uncheck all checkboxes except the one that was clicked
            checkboxes.forEach(cb => {
                if (cb !== checkbox) {
                    cb.checked = false;
                }
            });
        });
    }); 
})
<<<<<<< HEAD
=======

>>>>>>> da86c773ca0cde7e739f650d2f5cf3d0d739e298
