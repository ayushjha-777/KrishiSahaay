import numpy as np
from tensorflow.keras.preprocessing import image
from PIL import Image


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

