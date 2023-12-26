import cv2
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
contours = grab_contours(contours)
for con in contours:
    if contourArea(con) > 10:
        x, y, width, height = boundingRect(con)
        rectangle(image1, x , y , width,height , (100, 200, 220), 2)
        rectangle(image2, x , y , width,height , (100, 200, 220), 2)
x = np.zeros((360, 10, 3), np.uint8)
result = np.hstack((image1, x, image2))
cv2.imshow("Result", result)


cv2.waitKey(0)
cv2.destroyAllWindows()

