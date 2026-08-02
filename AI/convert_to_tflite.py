"""
Convert the trained 5-class Keras model to TFLite for lightweight
deployment (same approach used for the original 3-class model on Render).

Run this locally where your .keras model file is:
    python convert_to_tflite.py

Requires: tensorflow (already installed since you just trained with it)
"""

import tensorflow as tf

# Using the best checkpoint from training (saved via ModelCheckpoint,
# monitor="val_accuracy", save_best_only=True)
MODEL_PATH = "models/potato_disease_model_5class.keras"
OUTPUT_PATH = "models/potato_disease_model_5class.tflite"

model = tf.keras.models.load_model(MODEL_PATH)

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

with open(OUTPUT_PATH, "wb") as f:
    f.write(tflite_model)

print(f"Converted successfully -> {OUTPUT_PATH}")
