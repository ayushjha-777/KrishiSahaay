import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

# Load trained model
model = tf.keras.models.load_model("models/potato_disease_model.keras")

class_names = [
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy"
]

# Image path
img_path = "test.jpg"

# Load image
img = image.load_img(
    img_path,
    target_size=(224, 224)
)

# Convert image to array
img_array = image.img_to_array(img)

# Add batch dimension
img_array = np.expand_dims(img_array, axis=0)

# Preprocess for MobileNetV2


# Predict
prediction = model.predict(img_array)
print(prediction)
for i, class_name in enumerate(class_names):
    print(f"{class_name}: {prediction[0][i] * 100:.2f}%")
# Get predicted class index
predicted_index = np.argmax(prediction)

# Get confidence
confidence = np.max(prediction) * 100

print(f"\nPrediction : {class_names[predicted_index]}")
print(f"Confidence : {confidence:.2f}%")

top3 = np.argsort(prediction[0])[::-1]

print("\nTop Predictions:")
for idx in top3:
    print(f"{class_names[idx]} : {prediction[0][idx]*100:.2f}%")