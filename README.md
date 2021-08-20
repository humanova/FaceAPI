# FaceAPI

Simple face detection API based on Flask and OpenCV.
Using SSDNet DNN model to detect faces.

## Usage
API expects an image URL or a base64 encoded image.

Sample JSON POST request to `/api/v1/detect_url`.
```json
{
	"url" : "https://calvarychapeluniversity.com/wp-content/uploads/2011/04/CCU-GROUP41.jpg",
	"threshold" : 0.7
}
``` 
Sample JSON POST request to `/api/v1/detect`.
```json
{
	"img" : "c2RzZHN...2RzZA==",
	"threshold" : 0.7
}
``` 
## API Response Format
FaceAPI response includes _boundry boxes of detected faces_, _total number of faces_ and _detection time_ (in milliseconds).
```json
{
    "bboxes": [
        {
            "x1": 26,
            "x2": 174,
            "y1": 11,
            "y2": 216
        },
        ...
        {
            "x1": 481,
            "x2": 635,
            "y1": 247,
            "y2": 450
        }
    ],
    "face_count": 6,
    "success": true,
    "time": 230
}
```
## API Wrapper Example

### Requesting and printing the response.
```python
from faceDet import detectionURLRequest, cropFaces, blurFaces
import cv2 

# stock photo including 7 clear faces
img = "https://cdn.psychologytoday.com/sites/default/files/styles/image-article_inline_full/public/field_blog_entry_teaser_image/people%20laughing_0.jpg"

# 1 - get API response
response, resp_time = detectionURLRequest(img, 0.7)

print("first bbox : ", response['bboxes'][0])
print("face count :", response['face_count'])
print("response time for first request(ms) :", resp_time)
```
```
first bbox :  {'x1': 62, 'x2': 151, 'y1': 103, 'y2': 235}
face count : 7
response time for first request(ms) : 582
```
### Using wrappers face blurer.

```python
# 2 - get blurred image
blur = blurFaces(img, 0.7, is_url=True)
cv2.imshow('blurred img', blur)
```

![blurred_image](http://puu.sh/DJ52A/1dc5e50c11.jpg)

### Using wrappers face cropper.
```python
# 3 - get cropped faces(img), face bboxes, and image itself
# iterate through and show faces
faces, bbox, image = cropFaces(img, 0.7)

i = 1
for face in faces:
    cv2.imshow(str(i), face)
    cv2.moveWindow(str(i), (i * 80) + 500, 500)
    i+=1

# wait for key press to destroy the windows
cv2.waitKey(0)
cv2.destroyWindow()
```

![blurred_image](http://puu.sh/DJ577/eb811e8345.jpg)
