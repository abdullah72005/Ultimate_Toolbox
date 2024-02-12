import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from helpers.convert import deleteFiles

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['UPLOAD_DIRECTORY'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #16MB
app.config['ALLOWED_EXTENSIONS'] = {'.jpg', '.jpeg', '.png', '.SVG', '.TIFF', '.TIFDoc', '.Docx', '.pdf', '.PPT', '.PPTX'}

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
            
            # Extract the file extension
            extension = os.path.splitext(file.filename)[1]

            # Check if a file is provided
            if file:
                # Check if the file extension is in the allowed extensions set
                if extension not in app.config['ALLOWED_EXTENSIONS']:
                    return 'File is not an allowed image type.'
                
                # Save the file to the specified directory
                file.save(os.path.join(
                    app.config['UPLOAD_DIRECTORY'],
                    secure_filename(file.filename)
                ))     
                # Convert file
                # delete file in folder 
                deleteFiles(app)
        # Handle the case where the file size exceeds the limit
        except RequestEntityTooLarge:
            return 'File is larger than the 16mb limit.'
        
        # Return a success message after the file has been uploaded
        return 'File has been uploaded successfully.'

