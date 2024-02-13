import os
import magic

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, send_file
from flask_session import Session
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from PIL import Image

from helpers.functions import apology, getOutputChoices
from helpers.convertion import convIMAGE


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# moved uploads to static file
app.config['UPLOAD_DIRECTORY'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #16MB

# updated all allowed file types per magic output
app.config['ALLOWED_EXTENSIONS'] = ['image/jpg', 'image/jpeg', 'image/png', 'image/avif', 'image/svg+xml', 'image/tiff', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/pdf', 'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation']

# add allowed image and text separate variables
app.config['IMAGE_EXTENTIONS'] = ['image/jpg', 'image/jpeg', 'image/png', 'image/avif', 'image/svg+xml', 'image/tiff']
app.config['TEXT_EXTENTIONS'] = ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/pdf', 'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation']
app.config['IMAGE'] = ['jpg', 'jpeg', 'png', 'avif', 'svg', 'tiff']
app.config['TEXT'] = ['doc', 'docx', 'pdf', 'ppt', 'pptx']

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/upload', methods=["GET", "POST"])
def upload():

    # If the request method is GET, render the conversion.html template
    if request.method == "GET":
       
        return render_template("upload.html")
    else:
            try:
                # Retrieve the file from the request
                file = request.files['file']

                # Check if a file is provided
                if not file:
                    return apology("please input file")
                
                # Save the file to the specified directory
                file.save(os.path.join(
                    app.config['UPLOAD_DIRECTORY'],
                    secure_filename(file.filename)
                ))

                extension: str = magic.from_file(app.config['UPLOAD_DIRECTORY'] + secure_filename(file.filename), mime=True) 

                # Check if the file extension is in the allowed extensions set
                if extension not in app.config['ALLOWED_EXTENSIONS']:

                    # load apology for invalid extenion and clear 
                    return apology("invalid file type")
                
            # Handle the case where the file size exceeds the limit
            except RequestEntityTooLarge:
                # load apology for invalid file size
                return apology('File is larger than the 16mb limit.')

            # make variable with desired output choices
            outputChoices = getOutputChoices(extension, app.config['IMAGE_EXTENTIONS'], app.config['TEXT_EXTENTIONS'], app.config['IMAGE'], app.config['TEXT'])

            # get file name
            fileName = os.path.splitext(secure_filename(file.filename))[0]
            fileExtention = os.path.splitext(secure_filename(file.filename))[1]
            finalname = str(fileName) + str(fileExtention)            
            # Return a success message and the select desired output 
            return render_template("conversion.html", outputChoices=outputChoices, fileName=finalname)

            


        
@app.route('/conversion', methods=["GET", "POST"])
def con():
    if request.method == "POST":
        # Get the list of files in the upload directory
        files = [file for file in os.listdir(app.config['UPLOAD_DIRECTORY']) if file != 'ignore.txt']
        # Get the user's choice from the form
        choice = request.form.get("choice")

        # Iterate through each file in the directory
        for file in files:
            fileName = os.path.splitext(secure_filename(file))[0]
            fileExtention = os.path.splitext(secure_filename(file))[1]
            finalname = str(fileName) + str(fileExtention)
            print(finalname)
            extension: str = magic.from_file(app.config['UPLOAD_DIRECTORY'] + finalname, mime=True) 

            # if user inputs an image
            if extension in app.config['IMAGE_EXTENTIONS']:

                # convert the image to the desired output
                outputFile = convIMAGE(fileName, file, app, choice)

            # if user inputs txt
            elif extension in app.config['TEXT_EXTENTIONS']:

                # TODO
                return redirect("/")

        return outputFile
    
    else:
        return render_template("upload.html")


