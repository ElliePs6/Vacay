function fetchProgressData() {
    fetch(`/vacayvue/balance-data/?ajax=true`) // Append a query parameter to indicate AJAX request
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch progress data');
            }
            return response.json();
        })
        .then(data => {
            if (!data.balance_data) {
                throw new Error('balance_data property is missing in the response');
            }
            data.balance_data.forEach(balanceItem => {
                const leaveType = balanceItem.leave_type;
                const usedDays = balanceItem.usedDays;
                const totalDays = balanceItem.totalDays;

                updateProgressCircle(leaveType, usedDays, totalDays);
            });
        })
        .catch(error => console.error('Error fetching progress data:', error));
}

document.addEventListener("DOMContentLoaded", function() {
    fetchProgressData();
});

function updateProgressCircle(leaveType, usedDays, totalDays) {
    const progressCircle = document.querySelector(`[data-leave-type="${leaveType}"]`);
    if (!progressCircle) {
        console.error('Progress circle not found for leave type:', leaveType);
        return;
    }

    const percentage = totalDays === 0 ? 0 : (usedDays / totalDays) * 100;
    const progressIndicator = progressCircle.querySelector('.progress-indicator');
    const progressText = progressCircle.querySelector('.progress-text');

    progressIndicator.style.width = percentage + '%';
    progressText.textContent = `(${usedDays}/${totalDays})`;
}

