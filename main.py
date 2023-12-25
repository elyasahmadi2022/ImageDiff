import numpy as np
import cv2
from PIL import Image
import imutils
def differ(im1, im2):
    differences = np.abs(im1 - im2)
    return differences
def loading_image(path1):
    try:
        imag1 = Image.open(path1)
        imag1 = imag1.convert('L')
        width1, height1 = imag1.size
        image1_to_matrix = np.zeros((height1, width1), np.uint8)
        for y in range(height1):
            for x in range(width1):
                pixel = imag1.getpixel((x,y))
                image1_to_matrix[y,x] = pixel

        return image1_to_matrix
    except IOError:
        print("Error, loading image")
        return None
def difference_image_to_binary(image, threshold):
    binary_image = []
    for row in image:
        binary_row = []
        for pixel in row:
            if pixel >= threshold:
                binary_row.append(255)  # White pixel
            else:
                binary_row.append(0)  # Black pixel
        binary_image.append(binary_row)
    # Dilation
    num_rows = len(binary_image)
    num_cols = len(binary_image[0])
    dilated_image = np.zeros((num_rows, num_cols), dtype=np.uint8)
    kernel = np.ones((5, 5), np.uint8)
    kernel_radius = kernel.shape[0] // 1

    for i in range(num_rows):
        for j in range(num_cols):
            if binary_image[i][j] == 255:
                for dx in range(-kernel_radius, kernel_radius + 1):
                    for dy in range(-kernel_radius, kernel_radius + 1):
                        new_x = i + dx
                        new_y = j + dy
                        if 0 <= new_x < num_rows and 0 <= new_y < num_cols:
                            dilated_image[new_x][new_y] = 255

    return dilated_image


def find_contours(binary_image):
    contours = []
    num_row, num_col = binary_image.shape
    visited = np.zeros((num_row,num_col), np.uint8)
    for i in range(num_row):
        for j in range(num_col):
            if binary_image[i,j] == 255 and visited[i,j] ==0:
                contour = []
                stack[(i,j)]
                while stack:
                    x,y = stack.pop()
                    if binary_image[x,y] == 255 and visited[x,y] == 0:
                        visited[x,y] = 1
                        contour.append((x,y))
                        neighors = []
                        for dx in [-1,0,1]:
                            for dy in [-1,0,1]:
                                new_x = x+dx
                                new_y = y +dy
                                if 0 <= new_x < num_row and 0<= new_y < num_col and visited[new_x, new_y] == 0:
                                    neighors.append((new_x, new_y))
                        if len(neighors) > 0:
                            stack.extend(neighors)
                contours.append(contour)
return contours
                    



path1 = 'O:\E\pyton\image1.png'
path2 = 'O:\E\pyton\image2.png'
image1 = loading_image(path1)
image2 = loading_image(path2)
image1 = cv2.resize(image1, (600,360))
image2 = cv2.resize(image2, (600,360))
# cv2.imshow("FirstImage", image1)
# cv2.imshow("SecondImage", image2)

differences = differ(image1, image2)
thresholding_value = 1
dilate = difference_image_to_binary(differences, thresholding_value)
cv2.imshow("Dilate", dilate)
cv2.imshow("Differences", differences)
kernel = np.ones((5,5), np.uint8)
contour = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# contour = find_contours(dilate)
# contour = get_bounding_boxes(contour)
contour = imutils.grab_contours(contour)
# contour = grab_contours(contour)
imag1 = cv2.cvtColor(image1,cv2.COLOR_GRAY2BGR)
imag2 = cv2.cvtColor(image2, cv2.COLOR_GRAY2BGR)
for con in contour:
    if cv2.contourArea(con) > 100:
        x,y,w,h = cv2.boundingRect(con)
        cv2.rectangle(imag1, (x,y), (x+w , y+h), (255,255,255), 2)
        cv2.rectangle(imag2, (x,y),(x+w , y+h), (0,0,255), 2)
x = np.ones((360,10,3), np.uint8)
result = np.hstack((imag1, x, imag2))
cv2.imshow("result", result)


cv2.waitKey(0)
cv2.destroyAllWindows()
