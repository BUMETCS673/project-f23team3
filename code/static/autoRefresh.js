let lastActivityTime = Date.now();
let countdownTime = 20000; // 20 seconds in milliseconds
let intervalId;

function checkActivity() {
    const currentTime = Date.now();
    const timeSinceLastActivity = currentTime - lastActivityTime;

    // Check if there's been inactivity for 20 seconds
    if (timeSinceLastActivity > countdownTime) {
        // No movement for 20 seconds, refresh the page
        location.reload();
    } else {
        // Activity detected, reset the timer and update the countdown
        lastActivityTime = currentTime;
        countdownTime = countdownTime - timeSinceLastActivity;

        // Update the countdown element if it exists
        const countdownElement = document.getElementById('countdown');
        if (countdownElement) {
            countdownElement.textContent = `Refresh in ${Math.floor(countdownTime / 1000)} seconds`;
        }
    }
}

// Attach event listeners to track user activity
document.addEventListener('mousemove', checkActivity);
document.addEventListener('keydown', checkActivity);
document.addEventListener('scroll', checkActivity);

// Start the countdown and check for activity every second
intervalId = setInterval(checkActivity, 1000);