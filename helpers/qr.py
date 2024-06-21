import pyqrcode

def convqr(link, output_path):
    # create the qrcode
    url = pyqrcode.create(link)
    url.png(output_path, scale = 20)
    return output_path