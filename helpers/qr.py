import pyqrcode
import png

from helpers.functions import deleteFiles


uploadFolder = 'static/uploads/'

def convqr(link, output_path):

    url = pyqrcode.create(link)
    url.png(output_path, scale = 8)
    return output_path


