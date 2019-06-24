# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import json
import requests
import cv2
import numpy as np
import time
from urllib.request import urlopen
import base64

API_URL = "https://hmnv-face-det.herokuapp.com/api/v1"

def detectionRequest(encrypted_img, threshold):
    
    content = {"img" : encrypted_img, "threshold" : threshold}
    try:
        start = time.clock()
        r = requests.post(f"{API_URL}/detect", timeout=4.0, json=content)
        resp_time = int((time.clock() - start) * 1000)
        response = r.json()
        
        if response['success'] == True:
            return response, resp_time
        else:
            return None, None
    except Exception as e:
        print(e)
        return None, None

def detectionURLRequest(img_url, threshold):
    
    if isImgURL(img_url):
        content = {"url" : img_url, "threshold" : threshold}
        try:
            start = time.clock()
            r = requests.post(f"{API_URL}/detect_url", timeout=4.0, json=content)
            resp_time = int((time.clock() - start) * 1000)
            response = r.json()

            if response['success'] == True:
                return response, resp_time
            else:
                return None, None
        except Exception as e:
            return e, None
    else:
        return None, None

def isImgURL(url):

    suffix_list = ['jpg', 'gif', 'png', 'tif', 'svg']
    file_name = url[url.rfind("/")+1:]
    file_suffix = file_name.split('.')[1]

    if file_suffix in suffix_list:
        return True
    else:
        return False

def decodeb64img(encoded_string, readFlag=cv2.IMREAD_COLOR):
    r = base64.b64decode(encoded_string)
    img_arr = np.frombuffer(r, dtype="uint8")
    img = cv2.imdecode(img_arr, readFlag)
    return img

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

def cropFaces(img, threshold, is_url = True):

    if is_url:
        resp, resp_time = detectionURLRequest(img, threshold)
    else:
        resp, resp_time = detectionRequest(img, threshold)
    ##print(f'response time : {resp_time}ms')
    ##print(f"detection time : {resp['time']}ms")
    ##print(f"face count : {resp['face_count']}")
    bboxes = resp['bboxes']
    face_count = int(resp['face_count'])

    if is_url:
        success, image = url2img(img)
    else:
        image = decodeb64img(img)
        success = True

    if success:
        faces = []
        for bbox in bboxes:
            face = image[bbox['y1']:bbox['y2'], bbox['x1']:bbox['x2']].copy()
            faces.append(face)
        return faces, bboxes, image
    else:
        return None

def blurFaces(img, threshold, is_url = True):
    faces, bbox, image = cropFaces(img, threshold)

    blurred_img = image
    if not faces == None:
        i = 0
        for face in faces:
            blurred_face = cv2.GaussianBlur(face, (23, 23), 30)
            blurred_img[bbox[i]['y1']:bbox[i]['y2'], bbox[i]['x1']:bbox[i]['x2']] = blurred_face
            i += 1

        return blurred_img
    else:
        return None