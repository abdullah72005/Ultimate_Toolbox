from googletrans import Translator
import os
from docx import Document
from flask import send_file
from helpers.functions import deleteFiles
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

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

        custom_font = TTFont('font-custom', 'static/NotoSans-VariableFont_wdth,wght.ttf')
        pdfmetrics.registerFont(custom_font)


        custom_ar = TTFont('ar-custom', 'static/IBMPlexSansArabic-Regular.ttf')
        pdfmetrics.registerFont(custom_ar)

        new_filename = f"{fileName}-{output_lang}.pdf"
        output_filepath = os.path.join(uploadFolder, new_filename)
        input_filepath = os.path.join(uploadFolder, f"{fileName}.pdf")

        file = open(input_filepath, 'rb')

        reader = PdfReader(file)
        translator = Translator()
        pn = len(reader.pages)

        

        c = canvas.Canvas(output_filepath, pagesize=letter)
        width, height = letter

        for p in range(pn):
            page = reader.pages[p]
            text = page.extract_text()

            transtxt = translator.translate(text, src=langs[input_lang], dest=langs[output_lang])
            output = transtxt.text
            # Replace newline characters with proper formatting
            output = output.replace('\n', '<br/>')
            # Replace special characters with spaces using Unicode replacement
            output = output.encode('utf-8', 'replace').decode('utf-8')
            # Split content by <br/> to handle newline characters
            lines = output.split('<br/>')
            # Write content to PDF
            for i, line in enumerate(lines):
                y_position = height - 50 - (i * 14)  # Adjust spacing

                #Strip leading spaces and then draw the line
                if translator.detect(line).lang == "ar":
                   c.setFont('ar-custom', 12)
                   # Draw Arabic text from right to left
                   c.drawRightString(width - 50, y_position, line[::-1])
                else:
                    c.setFont('font-custom', 12)
                    c.drawString(50, y_position, line.lstrip())
        c.save()

        # Create a Flask send_file response for downloading the translated document
        outputFile = send_file(output_filepath, as_attachment=True)

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
                srcLang = g.lang

                # Translate the paragraph from detect language to the output language
                output = translator.translate(paragraph.text, src=srcLang, dest=langs[output_lang]).text

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
