from __future__ import division
import cv2
import time
import sys


def detectFace(net, frame, conf_threshold):

    net_frame = frame.copy()
    frameHeight = net_frame.shape[0]
    frameWidth = net_frame.shape[1]
    blob = cv2.dnn.blobFromImage(net_frame, 1.0, (300, 300), [
                                 104, 117, 123], False, False)

    net.setInput(blob)
    detections = net.forward()
    faces = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            box = {'x1': x1, 'y1':  y1, 'x2': x2, 'y2': y2}
            faces.append({'frame': frame[y1:y2, x1:x2], 'bbox': box})
            # if out:
            #    cv2.rectangle(net_frame, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight/150)), 8)
    return faces

# pass img itself (cv2 img)
def detect(img, conf_threshold, create_out=0):

    if not conf_threshold >= 0 and conf_threshold <= 1:
        return None

    modelFile = "model/res10_300x300_ssd_iter_140000_fp16.caffemodel"
    configFile = "model/deploy.prototxt"
    net = cv2.dnn.readNetFromCaffe(configFile, modelFile)

    frame = img

    time_start = time.time()
    faces = detectFace(net, frame, conf_threshold)
    complete_time = int((time.time() - time_start) * 1000)

    result = {'faces': faces, 'time': complete_time}
    return result
