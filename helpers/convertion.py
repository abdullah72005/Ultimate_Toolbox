import os
import pandas as pd
from flask import send_file
from PIL import Image
from pydub import AudioSegment
from werkzeug.utils import secure_filename

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
    'audio/x-hx-aac-adts': 'aac',
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

csvtypes = {
    'text/csv': 'csv',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':'xlsx',
    'application/json': 'json'
}

def conImgtoImg(fileName, file, app, choice):
    # Construct the path to the input image file
    img_path = os.path.join(uploadFolder, file)

    # Open the image file using Pillow (PIL)
    img = Image.open(img_path)

    # Construct the path to the output PNG file
    png_path = os.path.join(uploadFolder, f"{fileName}.{choice}")
    choice2 = choice.upper()

    # Save the image as a PNG file
    img.save(png_path, choice2)

def getOutputChoices(extension, ime, txte, aue, csve, im, txt, au, csv):
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
        notto = ["aac", 'm4a', "amr"]
        x = [choice for choice in au if choice != audioTypes[extension] and choice not in notto]
        return x
    
    # if file is csv let output choices be csv options and remove the file extention
    if extension in csve:
        x = [choice for choice in csv if choice != csvtypes[extension]]
        return x 


def convIMAGE(fileName, file, app, choice):
    # Check the user's choice and perform the corresponding conversion
    
    # Convert image to PDF
    conImgtoImg(fileName, file, app, choice)
    pdf_path = os.path.join(uploadFolder, f"{fileName}.{choice}"
    )  

    # make variable with output file, delete files from local directory, return output file
    outputFile = send_file(pdf_path, as_attachment=True)
    deleteFiles(uploadFolder)
    return outputFile

        

def convTXT(fileName, file, app, choice):
    print('cat')

    
def convert_audio(input_file, extension, filename, choice):
    # get the audio path and Load the input audio file
    audio_path = os.path.join(uploadFolder, input_file)
    sound = AudioSegment.from_file(audio_path, format=audioTypes[extension])
    
    # get output filename and get its path
    output_filename = secure_filename(filename + '.' + choice)
    output_filepath = os.path.join(uploadFolder, output_filename)

    # Export the sound to the output format, delete files, and return the output file
    sound.export(output_filepath, format=choice)
    x = send_file(output_filepath, as_attachment=True)
    deleteFiles(uploadFolder)
    return x


def convert_csv(input_file, extension, filename, choice):
    input_path = os.path.join(uploadFolder, input_file)
    filetype = csvtypes[extension]
    output_filename = filename + '.' + choice
    output_path = os.path.join(uploadFolder, output_filename)

    # if input file is a csv file
    if filetype == 'csv':
        print('its a csv')

        # if choice is excel 
        if choice == 'xlsx':
            
            csv = pd.read_csv(input_path, encoding = "ISO-8859-1")
            ew = pd.ExcelWriter(output_path)
            csv.to_excel(ew)
            ew.close()
            x = send_file(output_path, as_attachment=True)
        
        # if he chooses json
        elif choice == 'json':

            csv = pd.read_csv(input_path, encoding = "ISO-8859-1")
            csv.to_json(output_path, indent = 1, orient = 'records')
            x = send_file(output_path, as_attachment=True)

    # if input file is a excel file
    elif filetype == 'xlsx':
        
        # if user chooses csv
        if choice == 'csv':
            
            xl = pd.read_excel(input_path)
            xl.to_csv(output_path, index=None, header=True)
            x = send_file(output_path, as_attachment=True)

        # if user chooses json
        elif choice == 'json':

            xl = pd.read_excel(input_path)
            xl.to_json(output_path, indent = 1, orient = 'records')
            x = send_file(output_path, as_attachment=True)

    # if input file type is json
    elif filetype == 'json':

        # if user chooses csv
        if choice == 'csv':

            js = pd.read_json(input_path)
            js.to_csv(output_path, index=None, header=True)
            x = send_file(output_path, as_attachment=True)

        # if choice is excel 
        elif choice == 'xlsx':
            js = pd.read_json(input_path)
            ew = pd.ExcelWriter(output_path)
            js.to_excel(ew)
            ew.close()
            x = send_file(output_path, as_attachment=True)


    deleteFiles(uploadFolder)
    return x



