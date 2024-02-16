import os
from flask import render_template

uploadFolder = 'static/uploads/'



def deleteFiles(app):

    # List all files in the uploads folder
    files = os.listdir(app)
    # Iterate over the files and remove them

    for file in files:
        if file != 'ignore.txt':
            file_path = os.path.join(app, file)
            os.remove(file_path)

# apology function for wrong input
def apology(message, code=400):

    # render apology
    return render_template("apology.html", top=code, bottom=message), code
