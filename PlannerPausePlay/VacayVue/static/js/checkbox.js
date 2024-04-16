    // Get all the checkboxes
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
