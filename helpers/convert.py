import os
from flask import Flask, flash, redirect, render_template, request, session

def deleteFiles(app):
    # app.config['UPLOAD_DIRECTORY'] was not innitialized
    uploadFolder = 'static/uploads/'
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