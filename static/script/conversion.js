document.addEventListener('DOMContentLoaded', function() {
    // Animating dots 
    const dotsElement = document.getElementById('dots');
    let dots = '';
    let dotCount = 0;

    const addDots = setInterval(() => {
        dotCount = (dotCount + 1) % 4; // Reset dot count after 3 dots
        dots = '.'.repeat(dotCount);   // Repeat the dots based on count
        dotsElement.textContent = dots;
    }, 500); // Adjust the interval speed (500ms = half a second)
});

// Select the  conError div
const errorDiv = document.querySelector('. conError');

// Add a click event listener
errorDiv.addEventListener('click', function() {
    // Toggle the display property
    if (errorDiv.style.display === 'none') {
        errorDiv.style.display = 'block';
    } else {
        errorDiv.style.display = 'none';
    }
});

// Show loading and hide error divs when the form is submitted
function showLoading(){
    document.getElementById(' conLoading').style.display = 'block';
    errorDiv.style.display = 'none';
};