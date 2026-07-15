import numpy as np
import cv2
from tensorflow.keras.preprocessing import image
from PIL import Image


def is_leaf_image(uploaded_file, green_ratio_threshold=0.12):
    """
    Heuristic check to reject images that are clearly not plant leaves.

    Leaves are dominated by green/yellow-green hues. We convert the image
    to HSV and measure what fraction of pixels fall in the
    green/yellow-green range. Random photos (people, walls, objects, etc.)
    almost never have this much green, so this filters them out before
    they ever reach the disease-prediction model.

    NOTE: This is a lightweight heuristic, not a true leaf classifier.
    It will not catch every non-leaf image (e.g. a green wall), but it
    solves the common case of random/unrelated photos being confidently
    misclassified as a disease.
    """
    uploaded_file.seek(0)
    img = Image.open(uploaded_file).convert("RGB")
    uploaded_file.seek(0)

    img_np = np.array(img)
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    # Hue range covering green to yellow-green (typical leaf colors),
    # including darker/duller shades seen in diseased leaves.
    lower_green = np.array([15, 25, 20])
    upper_green = np.array([95, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    green_ratio = float(np.count_nonzero(mask)) / mask.size

    return green_ratio >= green_ratio_threshold


def image_to_numpy(uploaded_file):
    """
    Converts uploaded image to model input.
    Output shape: (1, 224, 224, 3)
    """

    # Open image
    img = Image.open(uploaded_file).convert("RGB")

    # Resize to model input size
    img = img.resize((224, 224))

    # Convert to numpy array
    img_array = image.img_to_array(img)

    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)

    # IMPORTANT:
    # Do NOT use preprocess_input() here.
    # It is already inside the trained model.

    return img_array