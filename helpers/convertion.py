import os
from flask import send_file
from PIL import Image
import aspose.words as aw

from helpers.functions import conImgtoImg, deleteFiles

uploadFolder = 'static/uploads/'

def convIMAGE(fileName, file, app, choice):
    # Check the user's choice and perform the corresponding conversion
    if choice == 'pdf':

        # Convert image to PDF
        print("please help me part 2")
        conImgtoImg(fileName, file, app, choice)
        pdf_path = os.path.join(uploadFolder, f"{fileName}.pdf")  
        print("please kill me part 1")

        # make variable with output file, delete files from local directory, return output file
        outputFile = send_file(pdf_path, as_attachment=True)
        deleteFiles(uploadFolder)
        return outputFile
    elif choice == 'png':
        # Convert image to PNG
        conImgtoImg(fileName, file, app, choice)
        png_path = os.path.join(uploadFolder, f"{fileName}.png")

        # make variable with output file, delete files from local directory, return output file
        outputFile = send_file(png_path, as_attachment=True)
        deleteFiles(uploadFolder)
        return outputFile

def convTXT(fileName, file, app, choice):
    print('cat')

    
