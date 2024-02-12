import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['UPLOAD_DIRECTORY'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #16MB
app.config['ALLOWED_EXTENSIONS'] = ['.jpg', '.jpeg']

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/converstion', methods=["GET", "POST"])
def conversion():
    try:
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        if file:

            if extension not in app.config('ALLOWED_EXTENSIONS'):
                return 'file is not an image.'
            file.save(os.path.join(
                app.config['UPLOAD_DIRECTORY'],
                secure_filename(file.filename)
            ))
    except RequestEntityTooLarge:
        return 'File is larger than the 16mb limit.'
    
    return redirect('/')
