const txt = document.getElementById("txt");
const selectIn = document.getElementById("selectIn");
const selectOut = document.getElementById("selectOut");
const form = document.getElementById("form");


// var input_txt = '{{input_txt}}';

// if (input_txt) {
//     txt.textContent = input_txt;
// }

// Save values to localStorage on form submit
form.addEventListener('submit', (event) => {
    localStorage.setItem('txt', txt.value);
    localStorage.setItem('selectIn', selectIn.value);
    localStorage.setItem('selectOut', selectOut.value);
    console.log('Form submitted and values saved to localStorage');
});

// Load saved values from localStorage
if (localStorage.getItem('txt')) {
    txt.value = localStorage.getItem('txt');
    console.log(localStorage.getItem('txt'));
}

if (localStorage.getItem('selectIn')) {
    selectIn.value = localStorage.getItem('selectIn');
    console.log(localStorage.getItem('selectIn'));
}

if (localStorage.getItem('selectOut')) {
    selectOut.value = localStorage.getItem('selectOut');
    console.log(localStorage.getItem('selectOut'));
}

// Clear localStorage on page reload
window.addEventListener('load', () => {
    localStorage.removeItem('txt');
    localStorage.removeItem('selectIn');
});