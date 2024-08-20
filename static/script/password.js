
var slider = document.getElementById("myRange");
var output = document.getElementById("demo");
const form = document.getElementById("form");
const upper = document.getElementById("upper");
const lower = document.getElementById("lower");
const nums = document.getElementById("nums");
const syms = document.getElementById("syms");


output.innerHTML = slider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
output.innerHTML = this.value;
}
document.addEventListener("DOMContentLoaded", function() {
    let email =  "{{ password }}";
    // Select the button by its id
    document.getElementById('copy').addEventListener('click', function(){
        navigator.clipboard.writeText(email)
        const button = document.getElementById('copy');  
    });
});
// Set checkbox states based on saved values
slider.value = localStorage.getItem('output', slider.value);
output.innerHTML = localStorage.getItem('output', slider.value);
upper.checked = localStorage.getItem('upper') === 'true';
lower.checked = localStorage.getItem('lower') === 'true';
nums.checked = localStorage.getItem('nums') === 'true';
syms.checked = localStorage.getItem('syms') === 'true';

// Save values to localStorage on form submit
form.addEventListener('submit', (event) => {
    localStorage.setItem('output', slider.value);
    localStorage.setItem('upper', upper.checked);
    localStorage.setItem('lower', lower.checked);
    localStorage.setItem('nums', nums.checked);
    localStorage.setItem('syms', syms.checked);
});


document.getElementById('copy').addEventListener('click', function() {
var tooltip = document.getElementById('tooltip');
tooltip.classList.add('show');
setTimeout(function() {
    tooltip.classList.remove('show');
}, 2000);
});


