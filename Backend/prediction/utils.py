from PIL import Image
import numpy as np

def process_image(uploaded_file):

    image = Image.open(uploaded_file)

    image = image.convert('RGB')

    image = image.resize((224,224))

    image_array = np.array(image)

    image_array = image_array / 255.0

    return image_array
