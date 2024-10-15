const dropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("file");
const imgV = document.getElementById("img-view");
const ico = document.querySelector(".dragico");



inputFile.addEventListener("change", uploadImage);


function uploadImage(){
    this.form.submit();
}


document.body.addEventListener("dragover", function(e){
    e.preventDefault();
    dropArea.style.opacity = "0.9";
    ico.style.transform = "scale(1.15)";
});

document.body.addEventListener("drop", function(e){
    e.preventDefault();
    inputFile.files = e.dataTransfer.files;
    inputFile.form.submit();
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

// Select the ytError div
const errorDiv = document.querySelector('.uploadError');

// Add a click event listener
errorDiv.addEventListener('click', function() {
    // Toggle the display property
    if (errorDiv.style.display === 'none') {
        errorDiv.style.display = 'block';
    } else {
        errorDiv.style.display = 'none';
    }
});