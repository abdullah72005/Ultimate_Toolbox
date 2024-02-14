import os
from flask import render_template
from PIL import Image

uploadFolder = 'static/uploads/'

imagetypes = {
    'image/jpg': 'jpg',
    'image/jpeg': 'jpeg',
    'image/png': 'png',
    'image/avif': 'avif',
    'image/svg+xml': 'svg',
    'image/tiff': 'tiff'
}

txttypes = {
    'application/msword': 'doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
    'application/pdf': 'pdf',
    'application/vnd.ms-powerpoint': 'ppt',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'pptx'
}

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

# function that ensures user doesnt change to the same file type as if (jpg to jpg)
def remove_folder_type(test_list, item): 
  
    # using list comprehension loop on everything minus the file type 
    res = [i for i in test_list if i != item] 
    return res 

#def conIMGtoPDF(fileName, file, app):
#    # Construct the path to the input image file
#    img_path = os.path.join(uploadFolder, file)
#
#    # Open the image file using Pillow (PIL)
#    img = Image.open(img_path)
#
#    # Construct the path to the output PDF file
#    pdf_path = os.path.join(uploadFolder, f"{fileName}.pdf")
#
#    # Save the image as a PDF file
#    img.save(pdf_path, "PDF")
#
#def conIMGtoPNG(fileName, file, app):
#    # Construct the path to the input image file
#    img_path = os.path.join(uploadFolder, file)
#
#    # Open the image file using Pillow (PIL)
#    img = Image.open(img_path)
#
#    # Construct the path to the output PNG file
#    png_path = os.path.join(uploadFolder, f"{fileName}.png")
#
#    # Save the image as a PNG file
#    img.save(png_path, "PNG") 

def conImgtoImg(fileName, file, app, choice):
    # Construct the path to the input image file
    img_path = os.path.join(uploadFolder, file)

    # Open the image file using Pillow (PIL)
    img = Image.open(img_path)

    # Construct the path to the output PNG file
    png_path = os.path.join(uploadFolder, f"{fileName}.{choice}")
    print("please help")

    # Save the image as a PNG file
    img.save(png_path, choice.upper())
    print("help me")
def getOutputChoices(extension, ime, txte, im, txt):
    # if file is image let output choices be image options and remove the file extention
    if extension in ime:
        x = [choice for choice in im if choice != imagetypes[extension]] + ['pdf']
        print(imagetypes[extension])
        return x


    # if file is txt let output choices be txt options and remove the file extention
    if extension in txte:
        x = [choice for choice in txt if choice != txttypes[extension]]
        return x

#def pdfToDocx(filename, )