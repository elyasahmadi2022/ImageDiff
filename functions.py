import imutils
import numpy as np
import cv2
from PIL import Image

def loading_image(path):
    try:
        image = Image.open(path)
        image = image.convert('L')
        width, height = image.size
        image_to_matrix = np.zeros((height, width), np.uint8)
        for y in range(height):
            for x in range(width):
                pixel = image.getpixel((x,y))
                image_to_matrix[y,x] = pixel
        return image_to_matrix
    except IOError:
        print("Erorr , Loading image")
        return None
def diff_image(image1, image2):
    diff = np.abs(image1 - image2)
    return diff

def image_to_binary(image, treshold_value):
    binary_image = []
    for row in image:
        binary_row = []
        for pixel in row:
            if pixel >= treshold_value:
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

def finding_contour(binary_image):
    contours = []
    num_rows, num_cols = binary_image.shape
    visited = np.zeros((num_rows, num_cols), dtype=np.uint8)
    for i in range(num_rows):
        for j in range(num_cols):
            if binary_image[i, j] == 255 and visited[i, j] == 0:
                contour = []
                stack = [(i, j)]
                while stack:
                    x, y = stack.pop()
                    if binary_image[x, y] == 255 and visited[x, y] == 0:
                        visited[x, y] = 1
                        contour.append((x, y))
                        neighbors = []
                        for dx in [-1, 0, 1]:
                            for dy in [-1, 0, 1]:
                                new_x = x + dx
                                new_y = y + dy
                                if 0 <= new_x < num_rows and 0 <= new_y < num_cols and visited[new_x, new_y] == 0:
                                    neighbors.append((new_x, new_y))
                        if len(neighbors) > 0:
                            stack.extend(neighbors)
                contours.append(contour)
    return contours
def grab_contours(contours):
    grabbed_contours = []
    for contour in contours:
        if len(contour) > 0:
            num_points = len(contour)
            contour_matrix = np.zeros((num_points, 2), dtype=np.int32)
            for i, point in enumerate(contour):
                contour_matrix[i, 0] = point[1]
                contour_matrix[i, 1] = point[0]
            grabbed_contours.append(contour_matrix)
    return grabbed_contours