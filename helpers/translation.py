import googletrans
from googletrans import Translator
import os
from docx import Document
from flask import send_file
from helpers.functions import deleteFiles

uploadFolder = 'static/uploads/'

def translatetxt(input_txt, input_lang, output_lang, langs):
    translator = Translator()

    # if no input lang selected, detect input lang then translate and return translated txt
    if input_lang == 'detect':
        g = translator.detect(input_txt)
        input_lang = g.lang
        output = translator.translate(input_txt, src=input_lang, dest=langs[output_lang])
    else:
        output = translator.translate(input_txt, src=langs[input_lang], dest=langs[output_lang])
    
    return output.text

def trans_doc(input_file, extension, fileName, input_lang, output_lang, langs):

    if extension == 'application/pdf':
        print()
    elif extension == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':

        # Load the input Word document
        doc = Document(input_file)

        # Initialize the translator
        translator = Translator()

        # Create a new Word document to store the translated content
        new_document = Document()

        # Iterate through paragraphs in the input document
        for paragraph in doc.paragraphs:

            # Determine the source language if it is set to 'detect'
            srcLang = input_lang
            if srcLang == 'detect':
                g = translator.detect(paragraph.text)
                input_lang = g.lang

                # Translate the paragraph from detect language to the output language
                output = translator.translate(paragraph.text, src=input_lang, dest=langs[output_lang]).text

            else:
                # Translate the paragraph from the specified input language to the output language
                output = translator.translate(paragraph.text, src=langs[input_lang], dest=langs[output_lang]).text

            # Add the translated paragraph to the new document
            new_document.add_paragraph(output)

        # Save the translated document with a new filename
        new_filename = f"{fileName}-{output_lang}.docx"
        new_document.save(os.path.join(uploadFolder, new_filename))

        # Create a Flask send_file response for downloading the translated document
        word_path = os.path.join(uploadFolder, new_filename)
        outputFile = send_file(word_path, as_attachment=True)

    # Clean up the upload folder after processing
    deleteFiles(uploadFolder)

    # Return the Flask send_file response
    return outputFile
