import os
import magic

from flask import Flask, redirect, render_template, request, send_file
from flask_session import Session
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge




from helpers.functions import apology, deleteFiles
from helpers.convertion import convIMAGE, getOutputChoices, convert_audio, convert_csv, pdf2word, txt2word, txt2pdf, word2txt, pdf2txt


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# moved uploads to static file
app.config['UPLOAD_DIRECTORY'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #16MB

# updated all allowed file types per magic output
app.config['ALLOWED_EXTENSIONS'] = ['image/x-pcx', 'image/bmp', 'image/jpg','image/jpeg', 'image/gif', 'image/vnd.microsoft.icon',  'image/png', 'image/tiff', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/pdf', 'image/x-portable-pixmap', 'image/vnd.adobe.photoshop', 'image/webp', 'audio/x-wav', 'audio/mpeg', 'audio/x-hx-aac-adts',  'audio/x-m4a', 'audio/vnd.dolby.dd-raw', 'audio/amr', 'text/csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' , 'application/json', 'text/plain']

# add allowed image and text separate variables
app.config['IMAGE_EXTENTIONS'] = ['image/bmp','image/jpeg', 'image/png', 'image/jpg', 'image/tiff' , 'image/gif', 'image/vnd.microsoft.icon', 'image/x-pcx', 'image/x-portable-pixmap', 'image/vnd.adobe.photoshop', 'image/webp']
app.config['TEXT_EXTENTIONS'] = ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/pdf', 'text/plain']
app.config['AUDIO_EXTENTIONS'] = ['audio/x-wav', 'audio/mpeg', 'audio/x-hx-aac-adts', 'audio/x-m4a', 'audio/vnd.dolby.dd-raw', 'audio/amr']
app.config['CSV_EXTENTIONS'] = ['text/csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' , 'application/json']

app.config['IMAGE'] = ['bmp', 'gif', 'ico', 'jpeg', 'pcx', 'png', 'ppm', 'psd', 'tiff', 'webp']
app.config['AUDIO'] = ['wav', 'mp3', 'aac', 'm4a', 'ac3', 'amr']
app.config['TEXT'] = ['docx', 'pdf', 'txt']
app.config['CSV'] = ['csv', 'xlsx', 'json']



@app.route("/")
def index():
    return render_template("index.html")


@app.route('/upload', methods=["GET", "POST"])
def upload():

    # If the request method is GET, render the conversion.html template
    if request.method == "GET":
    

        # clean uploads directory and render template
        deleteFiles(app.config['UPLOAD_DIRECTORY'])
        return render_template("upload.html")
    else:
            try:
                # always start with cleaning upload directory to prevent errors
                deleteFiles(app.config['UPLOAD_DIRECTORY'])

                # Retrieve the file from the request
                file = request.files['file']

                # Check if a file is provided
                if not file:
                    return apology("please input file")
                
                input_filename = secure_filename(file.filename)
                print(input_filename)
                if input_filename == 'ignore.txt':
                    new_name = 'ignore2.txt'
                    os.rename(app.config['UPLOAD_DIRECTORY'] + input_filename, app.config['UPLOAD_DIRECTORY'] + new_name)

                
                # Save the file to the specified directory
                file.save(os.path.join(
                    app.config['UPLOAD_DIRECTORY'],
                    secure_filename(file.filename)
                ))

                extension: str = magic.from_file(app.config['UPLOAD_DIRECTORY'] + secure_filename(file.filename), mime=True)
                print(extension)

                # Check if the file extension is in the allowed extensions set
                if extension not in app.config['ALLOWED_EXTENSIONS']:

                    # Delete files in folder
                    deleteFiles(app.config['UPLOAD_DIRECTORY'])

                    # load apology for invalid extenion and clear 
                    return apology("invalid file type")
                
            # Handle the case where the file size exceeds the limit
            except RequestEntityTooLarge:
                
                # Delete files in folder
                deleteFiles(app.config['UPLOAD_DIRECTORY'])
                
                # load apology for invalid file size
                return apology('File is larger than the 16mb limit.')

            # make variable with desired output choices
            outputChoices = getOutputChoices(extension, app.config['IMAGE_EXTENTIONS'], app.config['TEXT_EXTENTIONS'], app.config['AUDIO_EXTENTIONS'],app.config['CSV_EXTENTIONS'], app.config['IMAGE'], app.config['TEXT'], app.config['AUDIO'], app.config['CSV'])

            # get file name
            fileName = os.path.splitext(secure_filename(file.filename))[0]
            fileExtention = os.path.splitext(secure_filename(file.filename))[1]
            finalname = str(fileName) + str(fileExtention)            
            # Return a success message and the select desired output 
            return render_template("conversion.html", outputChoices=outputChoices, fileName=finalname)

            


        
@app.route('/conversion', methods=["GET", "POST"])
def con():
    if request.method == "POST":
        try:
            # Get the list of files in the upload directory
            files = [file for file in os.listdir(app.config['UPLOAD_DIRECTORY']) if file != 'ignore.txt']

            # Get the user's choice from the form
            choice = request.form.get("choice")

            # Iterate through each file in the directory
            for file in files:
                fileName = os.path.splitext(secure_filename(file))[0]
                fileExtention = os.path.splitext(secure_filename(file))[1]
                finalname = str(fileName) + str(fileExtention)
                extension: str = magic.from_file(app.config['UPLOAD_DIRECTORY'] + finalname, mime=True) 
                

                # if user inputs an image
                if extension in app.config['IMAGE_EXTENTIONS']:

                    # convert the image to the desired output
                    outputFile = convIMAGE(fileName, file, app, choice)

                # if user inputs txt
                elif extension in app.config['TEXT_EXTENTIONS']:

                    if extension == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' and choice == 'pdf':
                        outputFile = 'word2pdf(finalname, fileName)'

                    if extension == "application/pdf" and choice == "docx":
                        outputFile = pdf2word(file, fileName, choice)

                    if extension == "text/plain" and choice == "docx":
                        outputFile = txt2word(file, fileName, choice)
                    
                    if extension == "text/plain" and choice == "pdf":
                        outputFile = txt2pdf(file, fileName, choice)

                    if extension == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" and choice == "txt":
                        outputFile = word2txt(file, fileName, choice)

                    if extension == "application/pdf" and choice == "txt":
                        outputFile = pdf2txt(file, fileName, choice)
                    
                # if user inputs audio
                elif extension in app.config['AUDIO_EXTENTIONS']:
    
                    # convert the audio to the desired output
                    outputFile = convert_audio(file, extension, fileName, choice)

                # if user inputs a csv
                elif extension in app.config['CSV_EXTENTIONS']:

                    # convert the csv file for the desired output
                    outputFile = convert_csv(file, extension, fileName, choice)
                    
            # return converted file
            return outputFile

        # handle exeptions and make sure to clear upload directory before every move
        except:
            deleteFiles(app.config['UPLOAD_DIRECTORY'])
            return apology("An error has happened")
    else:
        # clean uploads directory and render template
        deleteFiles(app.config['UPLOAD_DIRECTORY'])
        return render_template("upload.html")




if __name__ == '__main__':
    deleteFiles(app.config['UPLOAD_DIRECTORY'])
    app.run(debug=True)