document.addEventListener('DOMContentLoaded', function () {
    console.log("DOM fully loaded and parsed.");

    // Show the modal when the button is clicked
    const addCustomHolidayBtn = document.getElementById('addCustomHolidayBtn');
    if (addCustomHolidayBtn) {
        console.log("Add Custom Holiday button found.");
        addCustomHolidayBtn.addEventListener('click', function () {
            console.log("Add Custom Holiday button clicked.");
            $('#customHolidayModal').modal('show');
        });
    } else {
        console.log("Add Custom Holiday button not found.");
    }


    // Handle form submission
    const customHolidayForm = document.getElementById('customHolidayForm');
    if (customHolidayForm) {
        console.log("Custom Holiday form found.");
        customHolidayForm.addEventListener('submit', function (event) {
            event.preventDefault();
            console.log("Custom Holiday form submitted.");

            const form = this;
            const formData = new FormData(form);

            // Serialize form data to send it as JSON
            const jsonData = {};
            formData.forEach((value, key) => {
                jsonData[key] = value;
            });

            console.log("Form data:", jsonData);

            $.ajax({
                url: '/vacayvue/add_custom_holiday/',
                type: 'POST',
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                },
                data: JSON.stringify(jsonData),
                contentType: 'application/json',
                success: function (data) {
                    console.log("AJAX request successful.");
                    if (data.success) {
                        console.log("Holiday added successfully.");
                        $('#customHolidayModal').modal('hide'); // Hide the modal
                    } else {
                        console.log("Failed to add holiday.", data.errors);
                        // Display form errors if any
                        if (data.errors) {
                            const errorMessages = Object.values(data.errors).flat();
                            alert('Failed to add holiday:\n' + errorMessages.join('\n'));
                        } else {
                            alert('Failed to add holiday');
                        }
                    }
                },
                error: function (xhr, status, error) {
                    console.error('Error:', error);
                }
            });
        });
    } else {
        console.log("Custom Holiday form not found.");
    }

});