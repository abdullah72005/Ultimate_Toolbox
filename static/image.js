// Initialize Cropper and aspectRatio variables
let cropper;
let aspectRatio = 'free';

// Function to toggle slider visibility based on filter choice
function toggleSlider() {
    var choiceSelect = document.getElementById("outputChoice");
    var sliderLabel = document.getElementById("sliderLabel");
    var sliderInput = document.getElementById("slider");

    // Check if the selected option is "Blur"
    if (choiceSelect.value === "Blur") {
        sliderLabel.style.display = "block"; // Show slider label
        sliderInput.style.display = "block"; // Show slider input
    } else {
        sliderLabel.style.display = "none"; // Hide slider label
        sliderInput.style.display = "none"; // Hide slider input
    }
}

// Execute the following code when the window finishes loading
window.onload = function () {
    // Add a new entry to the browser's history stack with the same URL
    // This ensures that when the user navigates back, they stay on the same page
    window.history.pushState(null, '', window.location.href);

    // Listen for the popstate event, which occurs when the user navigates back or forward
    window.onpopstate = function () {
        // When the user navigates back, attempt to move forward in the history
        // This effectively prevents the user from going back to the previous page
        window.history.forward();
    };
};


// Function to show/hide filter and crop blocks
function showBlock(selectedBlock) {
    var filterBlock = document.getElementById("filterBlock");
    var cropBlock = document.getElementById("editBlock");

    // Show the selected block and hide the rest of the blocks
    if (selectedBlock === "filter") {
        cropBlock.style.display = "none"; // Hide crop block
        filterBlock.style.display = "block"; // Show filter block
    } else if (selectedBlock === "edit") {
        filterBlock.style.display = "none"; // Hide filter block
        cropBlock.style.display = "block"; // Show crop block

        // Initialize Cropper for image editing
        const img = document.getElementById('img');
        cropper = new Cropper(img, {
            aspectRatio: NaN, // Set aspect ratio to NaN for free cropping
            viewMode: 0, // Set view mode to 0 for unrestricted dragging and cropping
        });
    }
}

// Event listener for changing drag mode to 'crop'
document.getElementById('dragCrop').addEventListener('click', function() {
    cropper.setDragMode('crop'); // Set Cropper drag mode to 'crop'
});

// Event listener for changing drag mode to 'move'
document.getElementById('dragMove').addEventListener('click', function() {
    cropper.setDragMode('move'); // Set Cropper drag mode to 'move'
});

// Event listener for changing drag mode to 'none'
document.getElementById('dragNone').addEventListener('click', function() {
    cropper.setDragMode('none'); // Set Cropper drag mode to 'none'
});

// Event listener for applying changes
document.getElementById('apply').addEventListener('click', function() {
    var croppedCanvas = cropper.getCroppedCanvas(); // Get the cropped canvas
    if (!croppedCanvas) {
        console.error('Failed to crop image'); // Log an error message to the console
        return;
    }
    
    // Convert cropped canvas to data URL
    var croppedImageData = croppedCanvas.toDataURL();

    // Set the value of the hidden input field to the data URL
    document.getElementById('croppedImage').value = croppedImageData;

    // Set the value of the hidden input field to indicate that image is cropped
    var isCropped = document.getElementById('isCropped').value = 1;
});

// Event listener for downloading the cropped image
document.getElementById('download').addEventListener('click', function() {
    var fileName = document.getElementById("fileName").textContent; // Get the file name

    // Get the cropped canvas
    var croppedCanvas = cropper.getCroppedCanvas();

    // Create a temporary anchor element
    var downloadLink = document.createElement('a');

    // Set the href attribute to the data URL of the cropped image
    downloadLink.href = croppedCanvas.toDataURL();

    // Set the download attribute to specify the filename
    downloadLink.download = "New" + fileName;

    // Append the anchor element to the body
    document.body.appendChild(downloadLink);

    // Trigger a click event on the anchor element to prompt download
    downloadLink.click();

    // Remove the anchor element from the DOM
    document.body.removeChild(downloadLink);
});

// Event listener for rotating image clockwise
document.getElementById('rotateClockwise').addEventListener('click', function() {
    cropper.rotate(90); // Rotate clockwise by 90 degrees
});

// Event listener for rotating image counterclockwise
document.getElementById('rotateCounterclockwise').addEventListener('click', function() {
    cropper.rotate(-90); // Rotate counterclockwise by 90 degrees
});

// Event listener for changing aspect ratio
document.getElementById('aspectRatio').addEventListener('change', function() {
    aspectRatio = this.value;
    if (aspectRatio === 'free') {
        cropper.setAspectRatio(NaN); // Set to 'free' aspect ratio
    } else {
        const ratio = aspectRatio.split('/').map(Number);
        cropper.setAspectRatio(ratio[0] / ratio[1]);
    }
});

// Event listener for flipping the image horizontally
document.getElementById('flipHorizontal').addEventListener('click', function() {
    cropper.scaleX(-cropper.getData().scaleX || -1);
});

// Event listener for flipping the image vertically
document.getElementById('flipVertical').addEventListener('click', function() {
    cropper.scaleY(-cropper.getData().scaleY || -1);
});

// Initial setup
showBlock(document.getElementById("operationChoice").value); // Show initial block based on selected option
toggleSlider(); // Toggle slider visibility based on initial choice
