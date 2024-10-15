// Select the ytError div
const errorDiv = document.querySelector('.ytError');

// Show loading section when the form is submitted
function showLoading(){
    document.getElementById('ytLoading').style.display = 'block';
    errorDiv.style.display = 'none';
};

// Add a click event listener
errorDiv.addEventListener('click', function() {
    // Toggle the display property
    if (errorDiv.style.display === 'none') {
        errorDiv.style.display = 'block';
    } else {
        errorDiv.style.display = 'none';
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Check if there's a stored value for the 'type' radio button
    const storedType = sessionStorage.getItem('selectedType');
    if (storedType) {
        // Set the radio button based on the stored value
        document.querySelector(`input[name="type"][value="${storedType}"]`).checked = true;
    }
    // Add event listener to remember selected radio button
    const radioButtons = document.querySelectorAll('input[name="type"]');
    radioButtons.forEach(button => {
        button.addEventListener('change', function() {
            if (this.checked) {
                // Store the selected value in session storage
                sessionStorage.setItem('selectedType', this.value);
            }
        });
    });
});

// Prevent the user from changing the radio button selection after clicking convert button 
document.getElementById("convertButton").addEventListener("click", function() {
    const radios = document.querySelectorAll('input[name="type"]');
    radios.forEach(function(radio) {
        radio.addEventListener('click', function(event) {
            event.preventDefault();
        });
    });
});