from faceDet import detectionURLRequest, cropFaces, blurFaces
import cv2 

# stock photo including 7 clear faces
img = "https://cdn.psychologytoday.com/sites/default/files/styles/image-article_inline_full/public/field_blog_entry_teaser_image/people%20laughing_0.jpg"

# 1 - get API response
response, resp_time = detectionURLRequest(img, 0.7)

print("first bbox : ", response['bboxes'][0])
print("face count :", response['face_count'])
print("response time for first request(ms) :", resp_time)

# 2 - get blurred image
blur = blurFaces(img, 0.7, is_url=True)
cv2.imshow('blurred img', blur)

# 3 - get cropped faces(img), face bboxes, and image itself
# iterate through and show faces
faces, bbox, image = cropFaces(img, 0.7)

i = 1
for face in faces:
    cv2.imshow(str(i), face)
    cv2.moveWindow(str(i), (i * 80) + 500, 500)
    i+=1

cv2.waitKey(0)
cv2.destroyWindow()