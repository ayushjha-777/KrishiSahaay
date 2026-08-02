import tensorflow as tf
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix

# Load model - using the best checkpoint saved during training
model = tf.keras.models.load_model("models/potato_disease_model_5class.keras")

# Test dataset (held-out, never seen during training/validation - the
# real check of whether the model generalizes)
test_dataset = tf.keras.utils.image_dataset_from_directory(
    "dataset/test",
    image_size=(224, 224),
    batch_size=32,
    shuffle=False
)

class_names = test_dataset.class_names
print("Class order:", class_names)

# Predictions
predictions = model.predict(test_dataset)

predicted_labels = np.argmax(predictions, axis=1)

true_labels = np.concatenate(
    [labels.numpy() for _, labels in test_dataset]
)

print("\nConfusion Matrix:\n")
print(confusion_matrix(true_labels, predicted_labels))

print("\nClassification Report:\n")
print(classification_report(
    true_labels,
    predicted_labels,
    target_names=class_names
))