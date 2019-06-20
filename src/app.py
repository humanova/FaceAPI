import os
import flask
from flask import request, jsonify
import json
import base64

from get_image import request_image
import detector

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#takes base64 image and threshold value
@app.route('/api/v1/detect', methods=['POST'])
def detect():
    encoded_img = request.json['img']
    conf_threshold = float(request.json['threshold'])
    
    with open("img/imageToDetect.png", "wb") as fh:
        fh.write(base64.b64decode(encoded_img))

    res = detector.detect('img/imageToDetect.png', conf_threshold)

    face_count = len(res['faces'])
    if not res == None and face_count > 0:

        bboxes = []
        for face in res['faces']:
            bboxes.append(face['bbox'])

        return jsonify(dict(success=True, bboxes=bboxes, face_count = face_count, time=res['time']))
    else:
        return jsonify(dict(success=False))


#takes image url and threshold value
@app.route('/api/v1/detect_url', methods=['POST'])
def detect_url():
    img_url = request.json['url']
    conf_threshold = float(request.json['threshold'])

    success, filename = request_image(img_url)
    if success:
        res = detector.detect(filename, conf_threshold)

        face_count = len(res['faces'])
        if not res == None and face_count > 0:

            bboxes = []
            for face in res['faces']:
                bboxes.append(face['bbox'])
            
            return jsonify(dict(success=True, bboxes=bboxes, face_count = face_count, time=res['time']))
        else:
            return jsonify(dict(success=False))
    else:
        return jsonify(dict(success=False))

app.run(host='0.0.0.0', port=os.environ['PORT'])