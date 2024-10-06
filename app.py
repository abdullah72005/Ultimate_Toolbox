import os
import magic
import googletrans

import base64

from flask import Flask, redirect, render_template, request, send_file, session, jsonify, url_for
from flask_session import Session
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from pytube.exceptions import RegexMatchError, LiveStreamError, VideoUnavailable, VideoPrivate, VideoRegionBlocked, AgeRestrictedError, MembersOnly


from helpers.functions import apology, deleteFiles
from helpers.convertion import convIMAGE, getOutputChoices, convert_audio, convert_csv, pdf2word, txt2word, txt2pdf, word2txt, pdf2txt, word2pdf, imagetypes, audioTypes, txttypes, csvtypes
from helpers.password import generate_password
from helpers.qr import convqr
from helpers.yt import print_audio_streams, download_audio, get_video_info
from helpers.translation import translatetxt, trans_doc
from helpers.image import filterImg, filters_dic, cropImg


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
    deleteFiles(app.config['UPLOAD_DIRECTORY'])
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
                if input_filename == 's9k8o0p6d5r2f3i1l4e7t2e8x9t0f1o4r2u5m7t6e5n3o2d4i7s9c8o0m1p5u2t3e6r9i0n4t7e2r1e5l8a4e8t5c2o1n3s7e9c0t4e6t1u7r2p5i0s4i1c9s3u8m6v3o2l4u0t1p3o7r9a5c4t8e2x1t7r9a4o2r1n5a6d0i3p8i2s7c5o1r3d6o2v4a9t0i8o7n1s3.txt':
                    return apology("stop hacking our website")

                
                # Save the file to the specified directory
                file.save(os.path.join(
                    app.config['UPLOAD_DIRECTORY'],
                    secure_filename(file.filename)
                ))

                extension: str = magic.from_file(app.config['UPLOAD_DIRECTORY'] + secure_filename(file.filename), mime=True)
 
                # Check if the file extension is in the allowed extensions set
                if extension not in app.config['ALLOWED_EXTENSIONS'] + ['application/octet-stream']:

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

            # get file name
            fileName = os.path.splitext(secure_filename(file.filename))[0]
            fileExtention = os.path.splitext(secure_filename(file.filename))[1]
            finalname = str(fileName) + str(fileExtention)    

            if extension == "application/octet-stream":

                    # split text to get suffix (extesnsion)
                    ext = finalname.split('.')[-1]

                    # make a dict with all extention-type pairs
                    extDict = imagetypes
                    extDict.update(audioTypes)
                    extDict.update(txttypes)
                    extDict.update(csvtypes)
                    
                    # try to get extension 
                    value = [i for i in extDict if extDict[i]== ext]
                    extension = value[0]

                    # if no extension then filetype unsupported
                    if extension == None:
                         # Delete files in folder
                        deleteFiles(app.config['UPLOAD_DIRECTORY'])

                        # load apology for invalid extenion and clear 
                        return apology("invalid file type")


            # make variable with desired output choices
            outputChoices = getOutputChoices(extension, app.config['IMAGE_EXTENTIONS'], app.config['TEXT_EXTENTIONS'], app.config['AUDIO_EXTENTIONS'],app.config['CSV_EXTENTIONS'], app.config['IMAGE'], app.config['TEXT'], app.config['AUDIO'], app.config['CSV'])

                   
            # Return a success message and the select desired output 
            return render_template("conversion.html", outputChoices=outputChoices, fileName=finalname)

            


        
@app.route('/conversion', methods=["GET", "POST"])
def con():
    if request.method == "POST":
        try:
            # Get the list of files in the upload directory
            files = [file for file in os.listdir(app.config['UPLOAD_DIRECTORY']) if file !=     's9k8o0p6d5r2f3i1l4e7t2e8x9t0f1o4r2u5m7t6e5n3o2d4i7s9c8o0m1p5u2t3e6r9i0n4t7e2r1e5l8a4e8t5c2o1n3s7e9c0t4e6t1u7r2p5i0s4i1c9s3u8m6v3o2l4u0t1p3o7r9a5c4t8e2x1t7r9a4o2   r1n5a6d0i3p8i2s7c5o1r3d6o2v4a9t0i8o7n1s3.txt']
        
            # Get the user's choice from the form
            choice = request.form.get("choice")

            # Iterate through each file in the directory
            for file in files:
                fileName = os.path.splitext(secure_filename(file))[0]
                fileExtention = os.path.splitext(secure_filename(file))[1]
                finalname = str(fileName) + str(fileExtention)
                extension: str = magic.from_file(app.config['UPLOAD_DIRECTORY'] + finalname, mime=True) 


                if extension == "application/octet-stream":

                    # split text to get suffix (extesnsion)
                    ext = finalname.split('.')[-1]

                    # make a dict with all extention-type pairs
                    extDict = imagetypes
                    extDict.update(audioTypes)
                    extDict.update(txttypes)
                    extDict.update(csvtypes)
                    
                    # try to get extension 
                    value = [i for i in extDict if extDict[i]== ext]
                    extension = value[0]

                    # if no extension then filetype unsupported
                    if extension == None:
                         # Delete files in folder
                        deleteFiles(app.config['UPLOAD_DIRECTORY'])

                        # load apology for invalid extenion and clear 
                        return apology("invalid file type")


                # if user inputs an image
                if extension in app.config['IMAGE_EXTENTIONS']:

                    # convert the image to the desired output
                    outputFile = convIMAGE(fileName, file, app, choice)

                # if user inputs txt
                elif extension in app.config['TEXT_EXTENTIONS']:

                    if extension == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' and choice == 'pdf':
                        outputFile = word2pdf(file, fileName, choice)

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



@app.route('/password-generator', methods=["GET", "POST"])
def generate():
    if request.method == "POST":
        # start by cleaning the upload directory
        deleteFiles(app.config['UPLOAD_DIRECTORY'])

        # get password length
        password_length = request.form.get('length')

        # get user password choices
        upper: bool = request.form.get('upper')
        lower: bool = request.form.get('lower')
        nums: bool = request.form.get('nums')
        syms: bool = request.form.get('syms')

        # check user input
        if not password_length:
            return apology("please provide password length")
        
        if int(password_length) < 4:
            return apology("minimum password length is 4 characters")
        
        if int(password_length) > 128:
            return apology("maximum password length is 128 characters")
        
        if not upper and not lower and not nums and not syms:
            return apology("please choose one or more password characters")

        if not upper and not lower and not nums and not syms and not password_length:
            return apology("please provide input")
        
        # generate the password
        password = generate_password(int(password_length), upper, lower, nums, syms)

        # pass the password to the html
        return render_template("password.html", password=password)
        

    else:
        return render_template("password.html")


@app.route('/qrcode', methods=["GET", "POST"])
def Qr():
    if request.method == "POST":
        # start by cleaning the upload directory
        deleteFiles(app.config['UPLOAD_DIRECTORY'])

        # get input url
        url = request.form.get('link')
        
        # check input
        if not url:
            return apology("please enter url")
        
        # check input size
        if len(url) > 1000:
            return apology("input too big")
        
        
        # generate a filename and make path for qrcode
        filename = generate_password(4, False, True, False, False)
        output_path = os.path.join(app.config['UPLOAD_DIRECTORY'], filename + '.png')

        # create the qrcode
        convqr(url, output_path)

        return render_template("qr.html", qrcode=output_path, filename=filename)
        
    else:
        # start by cleaning the upload directory
        deleteFiles(app.config['UPLOAD_DIRECTORY'])

        return render_template("qr.html")


@app.route('/yt-to-mp3', methods=["GET", "POST"])
def url():
    if request.method == "POST":
        try:
            deleteFiles(app.config['UPLOAD_DIRECTORY'])
            # Retrieve YouTube URL from the form and store it in the session 
            youtube_url = request.form['url']
            fileType = request.form['type']
            session['url'] = youtube_url
            session['type'] = fileType
            # if isPlaylist(youtube_url):
            #    playlistName, totalFileSize = get_playlist_info(youtube_url)
            #    session['playlistName'] = playlistName
            #    return render_template('ytDownload.html', youtube_url=url, playlistName=playlistName, totalFileSize=totalFileSize)
            # else:
            # Get video information and store title in the session 
            title, author, views, rating, duration, publishDate, thumbnail_url = get_video_info(youtube_url)
            duration = "{:02}:{:02}".format(duration // 60, duration % 60)

            # Format the datetime object to dd:mm:yyyy
            publishDate = publishDate.strftime("%d/%m/%Y")

            views = f"{views:,}"
            
            session['title'] = title  
            
            # Get audio streams and store in the session
            audio_streams = print_audio_streams(youtube_url, fileType)
            session["audio_streams"] = audio_streams
            conversion = 1

            # Render template with video information
            return render_template('ytcon.html', youtube_url=url, title=title, author=author, views=views, rating=rating, duration=duration, publishDate=publishDate, thumbnail_url=thumbnail_url, audio_streams=audio_streams, fileType=fileType, conversion=conversion)

        #If there is an error get the Error message
        except AgeRestrictedError as e:
            session['error_message'] = "This video is age-restricted."

        except VideoRegionBlocked as e:
            session['error_message'] = "This video is region blocked."

        except VideoUnavailable as e:
            session['error_message'] = "This video is unavailable."

        except VideoPrivate as e:
            session['error_message'] = "This video is private."

        except LiveStreamError as e:
            session['error_message'] = "This is a live stream and cannot be downloaded."

        except MembersOnly as e:
            session['error_message'] = "This video is for members only."

        except RegexMatchError as e:
            session['error_message'] = "Please input a correct YouTube URL."

        except Exception as e:
            session['error_message'] = "An unexpected error occurred: "

        except RequestEntityTooLarge:
            # Delete files in folder
            deleteFiles(app.config['UPLOAD_DIRECTORY'])
            
            # load apology for invalid file size
            session['error_message'] = "File is larger than the 16mb limit."
        
        
        #return the webpage with the error message and delete files
        deleteFiles(app.config['UPLOAD_DIRECTORY'])    
        return render_template('ytcon.html', error_message=session['error_message'])

    else: 
        deleteFiles(app.config['UPLOAD_DIRECTORY'])
        return render_template("ytcon.html")

@app.route('/mp3-download', methods=["GET", "POST"])
def download():
    if request.method == "POST":
        deleteFiles(app.config['UPLOAD_DIRECTORY'])
        # Retrieve YouTube URL from the session
        youtube_url = session.get('url', None)

        # Retrieve audio streams from the session and filetype 
        audio_streams = session.get("audio_streams", None)
        fileType = session.get('type', None)

        # Counter for the selected audio stream
        i = 0
        
        # Retrieve selected audio quality from the form
        quality = request.form.get('quality')
        
        # Find the index of the selected audio stream
        for audio_stream in audio_streams:
            if quality == str(audio_stream):
                break
            i += 1
        
        # Retrieve video title from the session
        title = session.get('title', None)
        
        # Download audio and return the file path
        audioFile = download_audio(youtube_url, i, title, fileType)
        
        # Return the file
        return audioFile
    else:
        deleteFiles(app.config['UPLOAD_DIRECTORY'])
        return render_template("ytcon.html")




@app.route('/translation', methods=["GET", "POST"])
def translate():

    if request.method == "POST":

        # get user input
        input_txt = request.form.get('input_txt')
        output_lang = request.form.get('output_lang')
        input_lang = request.form.get('input_lang')

        # get all languages supported by googletrans
        langs = googletrans.LANGCODES


        # check input
        if not input_txt:
            return apology("please enter text to translate")
        if not output_lang:
            return apology('please choose a language to translate to')
        
        # if no input lang specified detect input lang
        if not input_lang:
            input_lang = 'detect'
        
        # translate input
        output = translatetxt(input_txt, input_lang, output_lang, langs)

        # load html with translated output
        return render_template("translate.html", langs=langs, output=output, input_txt=input_txt)

    else:
        # get all languages supported by googletrans and load html
        langs = googletrans.LANGCODES
        return render_template("translate.html", langs=langs)




@app.route('/doc-translation', methods=["GET", "POST"])
def translatedoc():

    if request.method == "POST":

        try:
            # always start with cleaning upload directory to prevent errors
            deleteFiles(app.config['UPLOAD_DIRECTORY'])

            # get user input
            input_file = request.files['input_file']
            output_lang = request.form.get('output_lang')
            input_lang = request.form.get('input_lang')
            langs = googletrans.LANGCODES
            x = 1 # flag


            # check input
            if not input_file:
                return apology("please enter text to translate")

            input_filename = secure_filename(input_file.filename)
            if input_filename == 's9k8o0p6d5r2f3i1l4e7t2e8x9t0f1o4r2u5m7t6e5n3o2d4i7s9c8o0m1p5u2t3e6r9i0n4t7e2r1e5l8a4e8t5c2o1n3s7e9c0t4e6t1u7r2p5i0s4i1c9s3u8m6v3o2l4u0t1p3o7r9a5c4t8e2x1t7r9a4o2r1n5a6d0i3p8i2s7c5o1r3d6o2v4a9t0i8o7n1s3.txt':
                return apology("stop hacking our website")

            if not output_lang:
                return apology('please choose a language to translate to')

            # if no input lang specified detect input lang
            if not input_lang:
                input_lang = 'detect'

            # Save the file to the specified directory
            input_file.save(os.path.join(
                app.config['UPLOAD_DIRECTORY'],
                input_filename
            ))
            extension: str = magic.from_file(app.config['UPLOAD_DIRECTORY'] + input_filename, mime=True)


            # Check if the file extension is in the allowed extensions set
            if extension not in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain']:

                if extension == 'application/octet-stream':

                    try:
                        ext = input_filename.split('.')[-1]
                        
                        if ext in ['txt', 'docx']:

                            x = 0
                            fileName = os.path.splitext(secure_filename(input_file.filename))[0]
                            outputFile = trans_doc(input_file, ext, fileName, input_lang, output_lang, langs)


                    except:
                        # Delete files in folder
                        deleteFiles(app.config['UPLOAD_DIRECTORY'])

                        # load apology for invalid extenion and clear 
                        return apology("please input another file")
                else:
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

        # x will be flagged if the item was an octec file type
        if x:
            fileName = os.path.splitext(secure_filename(input_file.filename))[0]
            outputFile = trans_doc(input_file, extension, fileName, input_lang, output_lang, langs)

        if outputFile == 1:
            return apology("more than 15,000 characters.")
        
        return outputFile

    else:
        deleteFiles(app.config['UPLOAD_DIRECTORY'])
        langs = googletrans.LANGCODES
        return render_template("transdocs.html", langs=langs)

                
@app.route('/image/upload', methods=["GET", "POST"])
def image():
    # If the request method is GET, render the image.html template
    if request.method == "GET":
        # Clean the uploads directory and render the image.html template
        deleteFiles(app.config['UPLOAD_DIRECTORY'])
        return render_template("image.html")
    
    else:
        try:
            # Always start with cleaning the upload directory to prevent errors
            deleteFiles(app.config['UPLOAD_DIRECTORY'])

            # Retrieve the file from the request
            file = request.files['file']

            # Check if a file is provided
            if not file:
                return apology("please input file")
            
            input_filename = secure_filename(file.filename)

            # Check if the filename is a specific value to prevent hacking attempts
            if input_filename == 's9k8o0p6d5r2f3i1l4e7t2e8x9t0f1o4r2u5m7t6e5n3o2d4i7s9c8o0m1p5u2t3r9i0n4t7e2r1e5l8a4e8t5c2o1n3s7e9c0t4e6t1u7r2p5i0s4i1c9s3u8m6v3o2l4u0t1p3o7r9a5c4t8e2x1t7r9a4o2r1n5a6d0i3p8i2s7c5o1r3d6o2v4a9t0i8o7n1s3.txt':
                return apology("stop hacking our website")

            # Create the file path where the uploaded file will be saved
            filePath = os.path.join(app.config['UPLOAD_DIRECTORY'], secure_filename(file.filename))
            session['filePath'] = filePath
            
            # Save the file to the specified directory
            file.save(filePath)

            # Determine the file extension using the magic library
            extension: str = magic.from_file(app.config['UPLOAD_DIRECTORY'] + secure_filename(file.filename), mime=True)

            # Check if the file extension is in the allowed extensions set
            if extension not in app.config['IMAGE_EXTENTIONS']:
                # Delete files in folder
                deleteFiles(app.config['UPLOAD_DIRECTORY'])

                # Return an apology for an invalid extension
                return apology("invalid file type")
            
        # Handle the case where the file size exceeds the limit
        except RequestEntityTooLarge:
            
            # Delete files in folder
            deleteFiles(app.config['UPLOAD_DIRECTORY'])

            # Return an apology for an invalid file size
            return apology('File is larger than the 16mb limit.')
        
        # Get the filename and save it in the session
        fileName = file.filename
        session['fileName'] = fileName
        imgPath = os.path.join("../", filePath)

        # Retrieve available filters
        filters = filters_dic

        # Return the imageFilter.html template with the filename, image path, and available filters
        return render_template("imageFilter.html", fileName=fileName, imgPath=imgPath, filters=filters)




    
@app.route('/image/filter', methods=["GET", "POST"])
def imageFilter():
    if request.method == "POST":

        # Dictionary containing filter options
        filters = filters_dic       

        # Retrieve file path and file name from session
        filePath = session['filePath']
        fileName = session['fileName']

        # Get the choice
        choice = request.form.get("choice")  # Get the selected filter choice

        original = request.form.get("original")

        if original:
            # If original button clicked display original image
            imgPath = f"../{filePath}"
            return render_template("imageFilter.html", fileName=fileName, imgPath=imgPath, filters=filters)

        if choice in filters:
            isCropped = request.form.get('isCropped')  # Find if the picture is cropped or not
            
                
            # Apply selected filter to the image
            if isCropped:
                print("I am here")
                # If image is already cropped, use the cropped image path and name
                filePath = session['croppedImgPath']
                fileName = session['croppedImgName']

            # Apply filter to the image
            outputPath = filterImg(filePath, choice, fileName)
            fileName = os.path.join("New" + fileName)
            imgPath = f"../{outputPath}"
            return render_template("imageFilter.html", fileName=fileName, imgPath=imgPath, filters=filters, isCropped=isCropped) 

        elif choice == 'downloadFilter': 
            # Get the latest fileName
            fileName = request.form.get("fileName")

            # If 'download' button is clicked, prepare image for download
            Newfile = os.path.join("static/uploads", "New" + fileName)
            if os.path.exists(Newfile):
                return send_file(Newfile, as_attachment=True)
            else:
                Newfile = os.path.join("static/uploads", fileName)
                return send_file(Newfile, as_attachment=True)
        
        elif choice == 'applyCrop':
            # If operation is 'edit', handle image cropping
            croppedImg = request.form.get('cropped_image')
            cropped_image_path, croppedImgName = cropImg(croppedImg ,fileName)
            
            # Store cropped image details in session
            session['croppedImgPath'] = cropped_image_path
            session['croppedImgName'] = croppedImgName

            # Save that the image is cropped in the HTML
            isCropped = 1

            croppedImgPath = f"../{cropped_image_path}"
            
            return render_template("imagefilter.html", fileName=croppedImgName, imgPath=croppedImgPath, filters=filters, isCropped=isCropped)
        else:
            return apology("Something went wrong")

    else:
        # If request method is 'GET', render default image.html template
        return render_template("image.html")
            
        
            
            

@app.route('/about', methods=["GET"])
def about():
    return render_template("about.html")


@app.route('/contact', methods=["GET"])
def contact():
    return render_template("contact.html")


if __name__ == '__main__':
    deleteFiles(app.config['UPLOAD_DIRECTORY'])
    app.run(debug=True)

