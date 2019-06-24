import os
import glob
import numpy as np
from urllib.request import urlopen
from urllib.parse import urlparse
import cv2
import base64

def url2img(url, readFlag=cv2.IMREAD_COLOR):
    
    suffix_list = ['.jpg', '.gif', '.png', '.tif', '.svg']

    path = urlparse(url)
    p, file_suffix = os.path.splitext(path.path)
    file_name = os.path.basename(p)

    if file_suffix in suffix_list:
        try:
            resp = urlopen(url)
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            image = cv2.imdecode(image, readFlag)
        except Exception as e:
            print("Error while getting image from url", e)
            return False, None
        return True, image


def decodeb64img(encoded_string, readFlag=cv2.IMREAD_COLOR):
    r = base64.b64decode(encoded_string)
    img_arr = np.frombuffer(r, dtype="uint8")
    img = cv2.imdecode(img_arr, readFlag)
    return img