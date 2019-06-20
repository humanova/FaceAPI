import os
import requests
from io import open as iopen

def request_image(file_url):
    suffix_list = ['jpg', 'gif', 'png', 'tif', 'svg']
    file_name = file_url[file_url.rfind("/")+1:]
    file_suffix = file_name.split('.')[1]
    
    i = requests.get(file_url)
    if file_suffix in suffix_list and i.status_code == 200:
        path = f"img/{file_name}"
        with iopen(path, 'wb') as file:
            return file.write(i.content), path
    else:
        return False, None