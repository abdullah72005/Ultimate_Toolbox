import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from helpers.convert import deleteFiles, apology, remove_folder_type

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# moved uploads to static file
app.config['UPLOAD_DIRECTORY'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #16MB

# edited a typo
app.config['ALLOWED_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.SVG', '.TIFF', '.TIF', '.Doc', '.Docx', '.pdf', '.PPT', '.PPTX']

# add allowed image and text separate variables
app.config['IMAGE_EXTENTIONS'] = ['.jpg', '.jpeg', '.png', '.SVG', '.TIFF', '.TIF']
app.config['TEXT_EXTENTIONS'] = ['.Doc', '.Docx', '.pdf', '.PPT', '.PPTX']

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/conversion', methods=["GET", "POST"])
def conversion():
    # If the request method is GET, render the conversion.html template
    if request.method == "GET":
        return render_template("conversion.html")
    else:
        try:
            # Retrieve the file from the request
            file = request.files['file']
            
            # Extract the file extension temporarly until we user python-magic
            extension: str = os.path.splitext(file.filename)[1]

            # Check if a file is provided
            if file:

                # Check if the file extension is in the allowed extensions set
                if extension not in app.config['ALLOWED_EXTENSIONS']:

                    # load apology for invalid extenion
                    return apology("invalid file type")
                
                # Save the file to the specified directory
                file.save(os.path.join(
                    app.config['UPLOAD_DIRECTORY'],
                    secure_filename(file.filename)
                ))     

            # make variable with desired output choices
            outputChoices = []

            # if file is image let output choices be image options and remove the file extention
            if extension in app.config['IMAGE_EXTENTIONS']:
                outputChoices = remove_folder_type(app.config['IMAGE_EXTENTIONS'], extension)

            # if file is txt let output choices be txt options and remove the file extention
            if extension in app.config['TEXT_EXTENTIONS']:
                outputChoices = remove_folder_type(app.config['TEXT_EXTENTIONS'], extension)



                # Convert file TODO


                # delete file in folder 
            deleteFiles(app)


        # Handle the case where the file size exceeds the limit
        except RequestEntityTooLarge:

            # load apology for invalid file size
            return apology('File is larger than the 16mb limit.')
        
        # Return a success message after the file has been uploaded
        return 'File has been uploaded successfully.'

