$(document).ready(function() {
    // Get the current URL
    var currentUrl = window.location.href;

    // Loop through each navbar link
    $('.nav-link').each(function() {
        // Get the URL of the link
        var linkUrl = $(this).attr('href');

        // Check if the link URL matches the current URL
        if (currentUrl.indexOf(linkUrl) !== -1) {
            // Remove 'active' class from all navbar links
            $('.nav-link').removeClass('active');

            // Add the 'active' class to the current link
            $(this).addClass('active');
        }
    });
});
