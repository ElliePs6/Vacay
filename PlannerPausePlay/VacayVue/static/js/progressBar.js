document.addEventListener("DOMContentLoaded", function() {
    var progressCirclesContainers = document.querySelectorAll('.progress-circle-container');

    progressCirclesContainers.forEach(function(container) {
        var progressCircles = container.querySelectorAll('.progress-circle');

        progressCircles.forEach(function(progressCircle) {
            var leaveType = progressCircle.dataset.leaveType;
            var usedDays = parseInt(progressCircle.dataset.usedDays);//γιατι ειναι αριθμοι και περιμενοι string
            var totalDays = parseInt(progressCircle.dataset.defaultDays);

            // Debugging: Log values
            console.log("Leave Type:", leaveType);
            console.log("Used Days:", usedDays);
            console.log("Total Days:", totalDays);

            // Check for NaN or division by zero
            if (isNaN(usedDays) || isNaN(totalDays) || totalDays === 0) {
                console.error("Invalid or missing data for leave type:", leaveType);
                return;
            }

            // Calculate percentage
            var percentage = (usedDays / totalDays) * 100;

            // Debugging: Log percentage
            console.log("Percentage:", percentage);

            var progressIndicator = progressCircle.querySelector('.progress-indicator');
            var progressText = progressCircle.querySelector('.progress-text');

            // Update progress circle style and text
            progressIndicator.style.width = percentage + '%';
            progressText.textContent = '(' + usedDays + '/' + totalDays + ')';

            // Display percentage if it's a valid number
            if (!isNaN(percentage)) {
                progressText.textContent += ' ' + Math.round(percentage) + '%';
            } else {
                progressText.textContent = 'N/A';
            }
        });
    });
});