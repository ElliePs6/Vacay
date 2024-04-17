document.addEventListener('DOMContentLoaded', function() {
    // Get all input containers
    const inputContainers = document.querySelectorAll('.input-container');

    // Loop through each input container
    inputContainers.forEach(container => {
        // Get the input element and input group text element
        const input = container.querySelector('.form-control');
        const inputGroupText = container.querySelector('.input-group-text');

        // Add focus event listener to the input
        input.addEventListener('focus', () => {
            // Hide the input
            input.style.display = 'none';
            // Show the input group text
            inputGroupText.style.display = 'block';
        });

        // Add blur event listener to the input
        input.addEventListener('blur', () => {
            // Show the input
            input.style.display = 'block';
            // Hide the input group text
            inputGroupText.style.display = 'none';
        });
    });
});
