import os
from flask import send_file
from PIL import Image

from helpers.functions import conIMGtoPDF, conIMGtoPNG, deleteFiles

uploadFolder = 'static/uploads/'

def convIMAGE(fileName, file, app, choice):
    # Check the user's choice and perform the corresponding conversion
    if choice == 'pdf':

        # Convert image to PDF
        conIMGtoPDF(fileName, file, app)
        pdf_path = os.path.join(uploadFolder, f"{fileName}.pdf")  

        # make variable with output file, delete files from local directory, return output file
        outputFile = send_file(pdf_path, as_attachment=True)
        deleteFiles(uploadFolder)
        return outputFile
    elif choice == 'png':
        # Convert image to PNG
        conIMGtoPNG(fileName, file, app)
        png_path = os.path.join(uploadFolder, f"{fileName}.png")

        # make variable with output file, delete files from local directory, return output file
        outputFile = send_file(png_path, as_attachment=True)
        print("1")
        deleteFiles(uploadFolder)
        print("2")
        return outputFile

    