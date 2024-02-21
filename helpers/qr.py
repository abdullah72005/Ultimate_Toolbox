import pyqrcode
import png
from urllib.parse import urlparse



def convqr(link, output_path):

    # create the qrcode
    url = pyqrcode.create(link)
    url.png(output_path, scale = 8)
    return output_path

# check if link is in valid format
def isvalid(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False