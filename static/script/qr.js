const button = document.getElementById('copy');

function downloadPNG() 
{
    // Create an image element
    var img = new Image();
    // Set the source of the image
    img.src = "{{ qrcode }}";
    // Create a link element
    var link = document.createElement('a');
    // Set the href attribute of the link to the data URL of the image
    link.href = img.src;
    // Set the download attribute of the link to the file name
    link.download = "{{ filename }}"; 
    // Simulate a click on the link to trigger the download
    link.click();
}