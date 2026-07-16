import numpy as np
import cv2
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
    # including duller/browner shades seen in diseased leaves.
    # Deliberately narrower than a naive "green" range so that random
    # photos (skin tones, sky, walls, general scenes) don't accidentally
    # score high enough to pass.
    lower_green = np.array([30, 40, 30])
    upper_green = np.array([85, 255, 220])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    green_ratio = float(np.count_nonzero(mask)) / mask.size

    return green_ratio >= green_ratio_threshold


def calculate_severity(uploaded_file):
    """
    Estimate how much of the leaf area is affected by disease, using
    color segmentation:

    1. `leaf_mask`  - all leaf-colored pixels (green + yellow + brown +
                      dark spots), separating the leaf from the background.
    2. `healthy_mask` - the subset of the leaf that is healthy green.
    3. `diseased_mask` = leaf_mask MINUS healthy_mask (spots, lesions,
                      yellowing, browning, blackened tissue).

    severity % = diseased pixels / total leaf pixels * 100

    NOTE: This is a color-based heuristic, not pixel-perfect lesion
    segmentation. It works well for the common early/late blight
    presentation (dark/brown spots and patches against green tissue),
    but lighting, background clutter, or unusual disease presentation
    can shift the estimate.
    """
    uploaded_file.seek(0)
    img = Image.open(uploaded_file).convert("RGB")
    uploaded_file.seek(0)

    img_np = np.array(img)
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    # Whole leaf: green through yellow/brown, plus dark near-black spots
    # (low value/brightness) that are still part of the leaf, not background.
    lower_leaf = np.array([8, 30, 15])
    upper_leaf = np.array([95, 255, 255])
    leaf_mask = cv2.inRange(hsv, lower_leaf, upper_leaf)

    # Clean up small speckle noise so isolated pixels don't skew the ratio.
    kernel = np.ones((5, 5), np.uint8)
    leaf_mask = cv2.morphologyEx(leaf_mask, cv2.MORPH_OPEN, kernel)
    leaf_mask = cv2.morphologyEx(leaf_mask, cv2.MORPH_CLOSE, kernel)

    leaf_pixel_count = int(np.count_nonzero(leaf_mask))
    if leaf_pixel_count == 0:
        return {
            "severity_percent": 0.0,
            "severity_level": "Unknown",
        }

    # Healthy tissue: green hues with reasonable saturation/brightness.
    lower_healthy = np.array([30, 40, 40])
    upper_healthy = np.array([90, 255, 255])
    healthy_mask = cv2.inRange(hsv, lower_healthy, upper_healthy)
    healthy_mask = cv2.bitwise_and(healthy_mask, leaf_mask)

    # Diseased tissue: leaf pixels that are NOT healthy green
    # (brown/yellow spots, dark lesions, blackened patches).
    diseased_mask = cv2.bitwise_and(leaf_mask, cv2.bitwise_not(healthy_mask))
    diseased_pixel_count = int(np.count_nonzero(diseased_mask))

    severity_percent = round(
        (diseased_pixel_count / leaf_pixel_count) * 100, 2
    )

    if severity_percent < 10:
        severity_level = "Mild"
    elif severity_percent < 30:
        severity_level = "Moderate"
    else:
        severity_level = "Severe"

    return {
        "severity_percent": severity_percent,
        "severity_level": severity_level,
    }


def image_to_numpy(uploaded_file):
    """
    Converts uploaded image to model input.
    Output shape: (1, 224, 224, 3)
    """

    # Open image
    img = Image.open(uploaded_file).convert("RGB")

    # Resize to model input size
    img = img.resize((224, 224))

    # Convert to numpy array (float32, same as tf.keras's img_to_array)
    img_array = np.array(img, dtype=np.float32)

    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)

    # IMPORTANT:
    # Do NOT use preprocess_input() here.
    # It is already inside the trained model.

    return img_array