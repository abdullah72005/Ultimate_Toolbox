const dropArea = document.getElementById("drop-areaTrans");
const inputFile = document.getElementById("file");
const imgV = document.getElementById("img-viewTrans");
const ico = document.querySelector(".dragicoTrans");
const txt = document.querySelector(".dragtxtTrans");
const docdisplay = document.getElementById("transdocdisplay");
const selectIn = document.getElementById("selectIn");
const selectOut = document.getElementById("selectOut");

let msg = document.getElementById("msg");


inputFile.addEventListener("change", uploadImage);


function uploadImage(){
    ico.style.display = "none";
    txt.style.display = "none";
    dropArea.style.display = "none";
    docdisplay.style.display = "block";
    let filename = inputFile.files[0].name;
    msg.innerHTML = filename; 
}


document.body.addEventListener("dragover", function(e){
    e.preventDefault();
    dropArea.style.opacity = "0.9";
    ico.style.transform = "scale(1.15)";
});

document.body.addEventListener("drop", function(e){
    e.preventDefault();
    inputFile.files = e.dataTransfer.files;
    
    if (inputFile == null){
        return;
    }
    
    let filename = inputFile.files[0].name;
    ico.style.display = "none";
    txt.style.display = "none";
    dropArea.style.display = "none";
    docdisplay.style.display = "block";
    msg.innerHTML = filename;         
});

document.body.addEventListener("dragleave", function(e){
    e.preventDefault();
    dropArea.style.opacity = "0.7";
    ico.style.transform = "scale(1)";
});

dropArea.addEventListener("mouseover", function(){
    dropArea.style.opacity = "0.8";
    ico.style.transform = "scale(1.15)";
});

dropArea.addEventListener("mouseout", function(){
    dropArea.style.opacity = "0.7";
    ico.style.transform = "scale(1)";
});


// Save values to localStorage on form submit
form.addEventListener('submit', (event) => {
localStorage.setItem('selectInDoc', selectIn.value);
localStorage.setItem('selectOutDoc', selectOut.value);
console.log('Form submitted and values saved to localStorage');
});

// Load saved values from localStorage
if (localStorage.getItem('selectInDoc')) {
selectIn.value = localStorage.getItem('selectInDoc');
console.log(localStorage.getItem('selectInDoc'));
}

if (localStorage.getItem('selectOutDoc')) {
selectOut.value = localStorage.getItem('selectOutDoc');
console.log(localStorage.getItem('selectOutDoc'));
}

window.addEventListener('load', () => {
localStorage.removeItem('selectOutDoc');
localStorage.removeItem('selectInDoc');
});