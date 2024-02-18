import os
from flask import send_file
from PIL import Image
from pydub import AudioSegment

from helpers.functions import deleteFiles

uploadFolder = 'static/uploads/'


# link magic file type input with actual file type input via dictionary
imagetypes = {
    'image/jpeg': 'jpeg',
    'image/png': 'png',
    'image/tiff': 'tiff',
    'image/gif': 'gif',
    'image/bmp': 'bmp',
    'image/vnd.microsoft.icon': 'ico',
    'image/x-pcx': 'pcx',
    'image/x-portable-pixmap': 'ppm',
    'image/vnd.adobe.photoshop': 'psd',
    'image/webp': 'webp'
}

audioTypes = {
    'audio/x-wav': 'wav',
    'audio/mpeg': 'mp3',
    'audio/ogg': 'ogg',
    'audio/x-hx-aac-adts': 'aac',
    'video/x-ms-asf': 'wma',
    'audio/ogg': 'opus',
    'audio/x-m4a': 'm4a',
    'audio/vnd.dolby.dd-raw': 'ac3',
    'audio/amr': 'amr'

}

txttypes = {
    'application/msword': 'doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
    'application/pdf': 'pdf',
    'application/vnd.ms-powerpoint': 'ppt',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'pptx'
}

def conImgtoImg(fileName, file, app, choice):
    # Construct the path to the input image file
    print(choice)
    img_path = os.path.join(uploadFolder, file)

    # Open the image file using Pillow (PIL)
    img = Image.open(img_path)

    # Construct the path to the output PNG file
    png_path = os.path.join(uploadFolder, f"{fileName}.{choice}")
    choice2 = choice.upper()

    # Save the image as a PNG file
    img.save(png_path, choice2)

def getOutputChoices(extension, ime, txte, aue, im, txt, au):
    # if file is image let output choices be image options and remove the file extention
    if extension in ime:
        x = [choice for choice in im if choice != imagetypes[extension] and choice not in ['pcx', 'psd']] + ['pdf']
        return x


    # if file is txt let output choices be txt options and remove the file extention
    if extension in txte:
        x = [choice for choice in txt if choice != txttypes[extension]]
        return x
    
    # if file is audio let output choices be audio options and remove the file extention
    if extension in aue:
        x = [choice for choice in au if choice != audioTypes[extension]]
        return x


def convIMAGE(fileName, file, app, choice):
    # Check the user's choice and perform the corresponding conversion
    
    # Convert image to PDF
    conImgtoImg(fileName, file, app, choice)
    pdf_path = os.path.join(uploadFolder, f"{fileName}.{choice}")  

    # make variable with output file, delete files from local directory, return output file
    outputFile = send_file(pdf_path, as_attachment=True)
    deleteFiles(uploadFolder)
    return outputFile

        

def convTXT(fileName, file, app, choice):
    print('cat')

    
def convert_audio(file, extension, output_filename, choice):
    # Load the input audio file
    sound = AudioSegment.from_file(file, format=audioTypes[extension])
    
    # Export the sound to the output format
    
    sound.export(output_filename, format=choice)
    outputFile = send_file(output_filename, as_attachment=True)
    deleteFiles(uploadFolder)
    return outputFile