import os
import magic

from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from PIL import Image


uploadFolder = 'static/uploads/'


def deleteFiles(app):
    # app.config['UPLOAD_DIRECTORY'] was not innitialized
    try:
        # List all files in the uploads folder
        files = os.listdir(uploadFolder)
        
        # Iterate over the files and remove them
        for file in files:
            file_path = os.path.join(uploadFolder, file)
            os.remove(file_path)
    
    except Exception as e:
        # Handle exceptions, e.g., if the folder doesn't exist
        return 'No files to delete'

# apology function for wrong input
def apology(message, code=400):

    # render apology
    return render_template("apology.html", top=code, bottom=message), code

# function that ensures user doesnt change to the same file type as if (jpg to jpg)
def remove_folder_type(test_list, item): 
  
    # using list comprehension loop on everything minus the file type 
    res = [i for i in test_list if i != item] 
    return res 

def conIMGtoPDF(fileName, file, app):
    # Construct the path to the input image file
    img_path = os.path.join(uploadFolder, file)

    # Open the image file using Pillow (PIL)
    img = Image.open(img_path)

    # Construct the path to the output PDF file
    pdf_path = os.path.join(uploadFolder, f"{fileName}.pdf")

    # Save the image as a PDF file
    img.save(pdf_path, "PDF")

def conIMGtoPNG(fileName, file, app):
    # Construct the path to the input image file
    img_path = os.path.join(uploadFolder, file)

    # Open the image file using Pillow (PIL)
    img = Image.open(img_path)

    # Construct the path to the output PNG file
    png_path = os.path.join(uploadFolder, f"{fileName}.png")

    # Save the image as a PNG file
    img.save(png_path, "PNG")