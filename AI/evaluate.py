import tensorflow as tf
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix

# Load model
model = tf.keras.models.load_model("models/potato_disease_model.keras")

# Validation dataset
validation_dataset = tf.keras.utils.image_dataset_from_directory(
    "dataset/validation",
    image_size=(224, 224),
    batch_size=32,
    shuffle=False
)

class_names = validation_dataset.class_names

# Predictions
predictions = model.predict(validation_dataset)

predicted_labels = np.argmax(predictions, axis=1)

true_labels = np.concatenate(
    [labels.numpy() for _, labels in validation_dataset]
)

print("\nConfusion Matrix:\n")
print(confusion_matrix(true_labels, predicted_labels))

print("\nClassification Report:\n")
print(classification_report(
    true_labels,
    predicted_labels,
    target_names=class_names
))