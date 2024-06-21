// Initialize copper and variables
let cropper = null;
let aspectRatio = 'free';
var operationChoice = document.getElementById("operationChoice");
var isEdit = 0;
var changes = 0; 


// Function to initialize cropper
function initializeCropper() {
    const img = document.getElementById('img');
    cropper = new Cropper(img, {
        aspectRatio: NaN, // Set aspect ratio to NaN for free cropping
        viewMode: 0, // Set view mode to 0 for unrestricted dragging and cropping
        autoCrop: false,
        dragMode: 'none'
    });
}

// Function to destroy cropper
function destroyCropper() {
    if (cropper !== null) {
        cropper.destroy();
        cropper = null;
    }
}

// Event listener for applying changes
function applyCrop() {
    var croppedCanvas = cropper.getCroppedCanvas(); // Get the cropped canvas
    if (!croppedCanvas) {
        console.error('Failed to crop image'); // Log an error message to the console
        return;
    }
    console.log("I am here");
    // Convert cropped canvas to data URL
    var croppedImageData = croppedCanvas.toDataURL();

    // Set the value of the hidden input field to the data URL
    document.getElementById('croppedImage').value = croppedImageData;

    // Set the value of the hidden input field to indicate that image is cropped
    var isCropped = document.getElementById('isCropped').value = 1;
};


// Function to show/hide filter and crop blocks
function showBlock(selectedBlock) {
    var filterBlock = document.getElementById("filterBlock");
    var cropBlock = document.getElementById("editBlock");
    var downloadFilter = document.getElementById("downloadFilter");
    var downloadCrop = document.getElementById("downloadCrop");

    // Show the selected block and hide the rest of the blocks
    if (selectedBlock === "filter") {
        destroyCropper()

        cropBlock.style.display = "none"; // Hide crop block
        filterBlock.style.display = "block"; // Show filter block

        downloadFilter.style.display = "block"; // Show downloadFilter button
        downloadCrop.style.display = "none"; // Hide downloadCrop button

    } else if (selectedBlock === "edit") {
        filterBlock.style.display = "none"; // Hide filter block
        cropBlock.style.display = "block"; // Show crop block

        downloadFilter.style.display = "none"; // Hide downloadFilter button
        downloadCrop.style.display = "block"; // Show downloadCrop button

        isEdit = 1;        
        operationChoice.value = "edit";

        initializeCropper()
    }
}

// Apply changes when filter tab is hit
function applyCropFilter() {
    console.log("I am there");
    var filterButton = document.getElementById('filterButton');
    
    // Check if the button has the 'active' class
    if (filterButton.classList.contains('active') || changes == 0) {
        filterButton.type = 'button'; // Set button type to 'button'
        showBlock('filter');
    } else {
        console.log("I am everywhere");
        filterButton.type = 'submit'; // Set button type to 'submit'

        // Execute applyCrop function
        applyCrop();

        // Show Filter Block
        showBlock('filter');
        changes = 0;
    }
}

// Event listener for rotating image clockwise
document.getElementById('rotateClockwise').addEventListener('click', function() {
    cropper.rotate(90); // Rotate clockwise by 90 degrees
    changes = 1;
});

// Event listener for rotating image counterclockwise
document.getElementById('rotateCounterclockwise').addEventListener('click', function() {
    cropper.rotate(-90); // Rotate counterclockwise by 90 degrees
    changes = 1;
});


// Event listener for flipping the image horizontally
document.getElementById('flipHorizontal').addEventListener('click', function() {
    cropper.scaleX(-cropper.getData().scaleX || -1);
    changes = 1;
});

// Event listener for flipping the image vertically
document.getElementById('flipVertical').addEventListener('click', function() {
    cropper.scaleY(-cropper.getData().scaleY || -1);
    changes = 1;
});

// Event listener for changing drag mode to 'crop'
document.getElementById('dragCrop').addEventListener('click', function() {
    cropper.setDragMode('crop'); // Set Cropper drag mode to 'crop'
    changes = 1;
});

// Event listener for changing drag mode to 'move'
document.getElementById('dragMove').addEventListener('click', function() {
    cropper.setDragMode('move'); // Set Cropper drag mode to 'move'
    changes = 1;
});



// Event listener for downloading the cropped image
document.getElementById('downloadCrop').addEventListener('click', function() {
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


const buttons = document.querySelectorAll('.topTabs button');

buttons.forEach(button => {
    button.addEventListener('click', () => {
        // Remove "active" class from all buttons
        buttons.forEach(btn => btn.classList.remove('active'));
        
        // Add "active" class to the clicked button
        button.classList.add('active');
    });
});


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

// Function to enable buttons after a delay
function enableButtons() {
    const buttons = document.querySelectorAll('.leftBoxesFilter');
    buttons.forEach(button => {
        button.disabled = false; // Enable button
    });
}

// Disable buttons on page load
window.onload = function() {
    const buttons = document.querySelectorAll('leftBoxesFilter');
    buttons.forEach(button => {
        button.disabled = true; // Disable button
    });

    // Enable buttons after 1 second (1000 milliseconds)
    setTimeout(enableButtons, 1000);
};


// // Function to toggle slider visibility based on filter choice
// function toggleSlider() {
//     var choiceSelect = document.getElementById("outputChoice");
//     var sliderLabel = document.getElementById("sliderLabel");
//     var sliderInput = document.getElementById("slider");

//     // Check if the selected option is "Blur"
//     if (choiceSelect.value === "Blur") {
//         sliderLabel.style.display = "block"; // Show slider label
//         sliderInput.style.display = "block"; // Show slider input
//     } else {
//         sliderLabel.style.display = "none"; // Hide slider label
//         sliderInput.style.display = "none"; // Hide slider input
//     }
// }

// // Toggle options box
// function toggleMenu() {

//     var menu = document.getElementById("selectOptions");

//     if (menu.style.maxWidth === "0px" || menu.style.maxWidth === "") {
//       menu.style.maxWidth = "200px"; // Change the width to whatever suits your design
//       cropper.setAspectRatio(NaN); // Set to 'free' aspect ratio
//     } else {
//       menu.style.maxWidth = "0px";
//     }
//   }

// toggleSlider(); // Toggle slider visibility based on initial choice


// // Function to change aspect ratio
// function changeRatio(aspectRatio) {
//     console.log("changeRatio called with:", aspectRatio);
//     var menu = document.getElementById("selectOptions");

//     if (!cropper) {
//         console.error("Cropper is not initialized.");
//         return; // Do nothing if cropper is not initialized
//     }

//     if (aspectRatio === 'free') {
//         menu.style.maxWidth = "0px";
//         cropper.setAspectRatio(NaN); // Set to 'free' aspect ratio
//     } else {
//         menu.style.maxWidth = "0px";
//         cropper.setAspectRatio((aspectRatio));
//     }
// }
