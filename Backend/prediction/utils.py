import numpy as np
import cv2
from PIL import Image

def image_to_numpy(uploaded_file):
    """
    Converts uploaded image to model input.
    Output shape: (1, 224, 224, 3)
    """

    uploaded_file.seek(0)

    # Open image and convert to RGB
    img = Image.open(uploaded_file).convert("RGB")

    # Reset file pointer so the same uploaded file
    # can be reused by validation/severity functions
    uploaded_file.seek(0)

    # Resize according to MobileNetV2 input
    img = img.resize((224, 224))

    # Convert PIL image to NumPy array
    img_array = np.array(img, dtype=np.float32)

    # Add batch dimension:
    # (224,224,3) -> (1,224,224,3)
    img_array = np.expand_dims(img_array, axis=0)

    # IMPORTANT:
    # Do NOT call preprocess_input() here.
    # Preprocessing is already included inside the trained model.

    return img_array
# ============================================================
# LEAF IMAGE VALIDATION
# ============================================================

def is_leaf_image(uploaded_file, green_ratio_threshold=0.12):
    """
    Checks whether the uploaded image is likely to contain a leaf.

    Returns:
        True  -> likely leaf image
        False -> likely invalid/non-leaf image
    """

    uploaded_file.seek(0)

    img = Image.open(uploaded_file).convert("RGB")

    uploaded_file.seek(0)

    img_np = np.array(img)

    # Convert RGB -> BGR -> HSV
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    # Broad green range for leaf detection
    lower_green = np.array([20, 30, 20])
    upper_green = np.array([95, 255, 255])

    green_mask = cv2.inRange(
        hsv,
        lower_green,
        upper_green
    )

    total_pixels = green_mask.size
    green_pixels = cv2.countNonZero(green_mask)

    if total_pixels == 0:
        return False

    green_ratio = green_pixels / total_pixels

    return green_ratio >= green_ratio_threshold


# ============================================================
# MULTI-FACTOR SEVERITY ESTIMATION
# ============================================================

def calculate_severity(uploaded_file):
    uploaded_file.seek(0)

    img = Image.open(uploaded_file).convert("RGB")

    uploaded_file.seek(0)

    img_np = np.array(img)

    img_bgr = cv2.cvtColor(
        img_np,
        cv2.COLOR_RGB2BGR
    )

    hsv = cv2.cvtColor(
        img_bgr,
        cv2.COLOR_BGR2HSV
    )


    # ========================================================
    # STEP 1: LEAF SEGMENTATION
    # ========================================================

    lower_leaf = np.array([8, 30, 15])
    upper_leaf = np.array([95, 255, 255])

    leaf_mask = cv2.inRange(
        hsv,
        lower_leaf,
        upper_leaf
    )

    # Remove small noise and fill small gaps
    kernel = np.ones(
        (5, 5),
        np.uint8
    )

    leaf_mask = cv2.morphologyEx(
        leaf_mask,
        cv2.MORPH_OPEN,
        kernel
    )

    leaf_mask = cv2.morphologyEx(
        leaf_mask,
        cv2.MORPH_CLOSE,
        kernel
    )


    # --------------------------------------------------------
    # COUNT LEAF PIXELS
    # --------------------------------------------------------

    leaf_pixel_count = int(
        np.count_nonzero(leaf_mask)
    )

    if leaf_pixel_count == 0:

        return {
            "severity_percent": 0.0,
            "severity_level": "Unknown",
            "breakdown": None,
        }


    # ========================================================
    # STEP 2: HEALTHY TISSUE SEGMENTATION
    # ========================================================

    # This range includes darker green tissue and vein shadows
    # so that they are not incorrectly classified as lesions.

    lower_healthy = np.array(
        [20, 40, 25]
    )

    upper_healthy = np.array(
        [90, 255, 255]
    )

    healthy_mask = cv2.inRange(
        hsv,
        lower_healthy,
        upper_healthy
    )

    # Healthy pixels should only exist inside the leaf
    healthy_mask = cv2.bitwise_and(
        healthy_mask,
        leaf_mask
    )


    # ========================================================
    # STEP 3: DISEASED REGION EXTRACTION
    # ========================================================

    diseased_mask = cv2.bitwise_and(
        leaf_mask,
        cv2.bitwise_not(healthy_mask)
    )


    # ========================================================
    # STEP 4: REMOVE THIN VEIN / SHADOW ARTIFACTS
    # ========================================================

    thin_line_kernel = np.ones(
        (3, 3),
        np.uint8
    )

    # Erosion removes thin lines
    diseased_mask = cv2.erode(
        diseased_mask,
        thin_line_kernel,
        iterations=1
    )

    # Dilation restores genuine lesion blobs
    diseased_mask = cv2.dilate(
        diseased_mask,
        thin_line_kernel,
        iterations=1
    )


    # ========================================================
    # FEATURE 1: LESION AREA
    # ========================================================

    diseased_pixel_count = int(
        np.count_nonzero(diseased_mask)
    )

    area_percent = (
        diseased_pixel_count
        / leaf_pixel_count
    ) * 100


    # ========================================================
    # STEP 5: FIND LESION CONTOURS
    # ========================================================

    contours, _ = cv2.findContours(
        diseased_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    MIN_LESION_AREA_PX = 40

    candidate_contours = [
        c
        for c in contours
        if cv2.contourArea(c)
        >= MIN_LESION_AREA_PX
    ]


    # ========================================================
    # STEP 6: SHAPE FILTER
    # ========================================================

    def is_blob_shaped(contour):

        area = cv2.contourArea(
            contour
        )

        hull = cv2.convexHull(
            contour
        )

        hull_area = cv2.contourArea(
            hull
        )

        solidity = (
            area / hull_area
            if hull_area > 0
            else 0
        )

        rect = cv2.minAreaRect(
            contour
        )

        rw, rh = rect[1]

        long_side = max(
            rw,
            rh
        )

        short_side = min(
            rw,
            rh
        )

        aspect_ratio = (
            long_side / short_side
            if short_side > 0
            else float("inf")
        )

        # Thin elongated structures are more likely
        # to be veins or shadows than actual lesions.

        looks_like_thin_line = (
            aspect_ratio > 4
            and solidity < 0.5
        )

        return not looks_like_thin_line


    lesion_contours = [
        c
        for c in candidate_contours
        if is_blob_shaped(c)
    ]


    # ========================================================
    # FEATURE 2: LESION COUNT
    # ========================================================

    lesion_count = len(
        lesion_contours
    )


    # ========================================================
    # FEATURE 3: AVERAGE LESION SIZE
    # ========================================================

    lesion_areas = [
        cv2.contourArea(c)
        for c in lesion_contours
    ]

    if lesion_areas:

        avg_lesion_size = float(
            np.mean(lesion_areas)
        )

    else:

        avg_lesion_size = 0.0


    # ========================================================
    # NORMALIZED LESION COUNT SCORE
    # ========================================================

    MAX_LESIONS_FOR_FULL_SCORE = 20

    count_score = min(
        lesion_count
        / MAX_LESIONS_FOR_FULL_SCORE,
        1.0
    ) * 100


    # ========================================================
    # FEATURE 4: LESION COLOUR / DARKNESS
    # ========================================================

    if lesion_contours:

        lesion_mask = np.zeros_like(
            diseased_mask
        )

        cv2.drawContours(
            lesion_mask,
            lesion_contours,
            -1,
            255,
            -1
        )

        lesion_pixels_hsv = hsv[
            lesion_mask > 0
        ]

        mean_value = float(
            np.mean(
                lesion_pixels_hsv[:, 2]
            )
        )

        # Darker lesions receive higher severity score
        color_score = (
            1 - mean_value / 255
        ) * 100

    else:

        color_score = 0.0


    # ========================================================
    # FEATURE 5: LESION DISTRIBUTION
    # ========================================================

    if lesion_count >= 2:

        centroids = []

        for c in lesion_contours:

            m = cv2.moments(c)

            if m["m00"] != 0:

                centroids.append(
                    (
                        m["m10"] / m["m00"],
                        m["m01"] / m["m00"]
                    )
                )


        centroids = np.array(
            centroids
        )


        # Only calculate distribution if at least
        # two valid centroids were found.

        if len(centroids) >= 2:

            x, y, w, h = cv2.boundingRect(
                leaf_mask
            )

            leaf_diagonal = np.sqrt(
                w ** 2 + h ** 2
            )

            spread = np.std(
                centroids,
                axis=0
            )

            spread_magnitude = np.sqrt(
                spread[0] ** 2
                + spread[1] ** 2
            )

            distribution_score = min(
                spread_magnitude
                / (
                    leaf_diagonal / 2
                    + 1e-6
                ),
                1.0
            ) * 100

        else:

            distribution_score = 0.0

    else:

        distribution_score = 0.0


  # ========================================================
# FINAL MULTI-FACTOR SEVERITY SCORE
# ========================================================

# Lesion area provides the baseline severity.
# Other factors adjust the baseline depending on
# lesion number, darkness and spatial spread.

    secondary_score = (
    0.40 * count_score
    + 0.25 * color_score
    + 0.35 * distribution_score
)

# Convert secondary information into a correction.
# 50 = neutral
# >50 increases severity
# <50 decreases severity
    correction = (secondary_score - 50) * 0.20

    severity_score = area_percent + correction

# Keep score between 0 and 100
    severity_score = round(
    min(max(severity_score, 0), 100),
    2
)
    # ========================================================
    # SEVERITY CLASSIFICATION
    # ========================================================

    if severity_score < 10:

        severity_level = "Mild"

    elif severity_score < 30:

        severity_level = "Moderate"

    else:

        severity_level = "Severe"


    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {

        "severity_percent":
            severity_score,

        "severity_level":
            severity_level,

        "breakdown": {

            "lesion_area_percent":
                round(
                    area_percent,
                    2
                ),

            "lesion_count":
                lesion_count,

            "avg_lesion_size_px":
                round(
                    avg_lesion_size,
                    1
                ),

            "color_severity_score":
                round(
                    color_score,
                    2
                ),

            "distribution_score":
                round(
                    distribution_score,
                    2
                ),
        },
    }