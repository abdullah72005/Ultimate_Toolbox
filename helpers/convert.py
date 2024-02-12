import os
from flask import Flask, flash, redirect, render_template, request, session

def deleteFiles(app):
    uploadFolder = app.config['UPLOAD_DIRECTORY']
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
