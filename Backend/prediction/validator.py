import cv2
import numpy as np


def variance_of_laplacian(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()


def edge_density(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 80, 180)
    return np.sum(edges > 0) / edges.size


def is_leaf_image(image):

    img = image.copy()

    if img.dtype != np.uint8:
        img = (img * 255).astype(np.uint8)

    img = cv2.resize(img, (224, 224))

    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    lower_green = np.array([25, 40, 40])
    upper_green = np.array([95, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)

    green_ratio = np.sum(mask > 0) / mask.size

    if green_ratio < 0.12:
        return False

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    if len(contours) == 0:
        return False

    largest = max(contours, key=cv2.contourArea)

    area = cv2.contourArea(largest)

    if area < 6000:
        return False

    contour_ratio = area / (224 * 224)

    if contour_ratio < 0.18:
        return False

    blur = variance_of_laplacian(img)

    if blur < 40:
        return False

    density = edge_density(img)

    if density < 0.015 or density > 0.35:
        return False

    return True