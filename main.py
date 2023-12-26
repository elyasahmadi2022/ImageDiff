import imutils
import numpy as np
import cv2
from PIL import Image
from functions import *



path1 ='O:\E\pyton\image1.png'

path2 ='O:\E\pyton\image2.png'
image1 = loading_image(path1)
image1 = cv2.resize(image1, (600, 360))
image2 = loading_image(path2)
image2 = cv2.resize(image2, (600, 360))
diff = diff_image(image1, image2)
value = 50
binary = image_to_binary(diff, value)
cv2.imshow("Binary", binary)
image1 = cv2.cvtColor(image1, cv2.COLOR_GRAY2RGB)
image2 = cv2.cvtColor(image2, cv2.COLOR_GRAY2RGB)
contours = finding_contour(binary)
# contours = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# contours = imutils.grab_contours(contours)
contours = grab_contours(contours)
for con in contours:
    if cv2.contourArea(con) > 100:
        x, y, w, h = cv2.boundingRect(con)
        cv2.rectangle(image1, (x, y), (x + w, y + h), (100, 200, 220), 2)
        cv2.rectangle(image2, (x, y), (x + w, y + h), (200, 0, 0), 2)

x = np.zeros((360, 10, 3), np.uint8)
result = np.hstack((image1, x, image2))
cv2.imshow("Result", result)


cv2.waitKey(0)
cv2.destroyAllWindows()

