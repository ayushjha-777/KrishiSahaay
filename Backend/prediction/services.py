import os
import logging
import numpy as np
from django.conf import settings

logger = logging.getLogger(__name__)

CLASS_NAMES = [
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
]

MODEL_PATH = os.path.join(
    settings.BASE_DIR,
    "prediction",
    "ml_models",
    "potato_disease_model.keras"
)


class ModelLoader:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            import tensorflow as tf   # <-- Lazy import

            logger.info("Loading AI model...")
            cls._model = tf.keras.models.load_model(MODEL_PATH)
            logger.info("Model loaded successfully.")

        return cls._model


def predict_disease(image_array):

    model = ModelLoader.get_model()

    prediction = model.predict(image_array, verbose=0)

    predicted_index = int(np.argmax(prediction))
    confidence = float(np.max(prediction) * 100)

    return {
        "prediction": CLASS_NAMES[predicted_index],
        "confidence": round(confidence, 2),
        "probabilities": {
            CLASS_NAMES[0]: round(float(prediction[0][0] * 100), 2),
            CLASS_NAMES[1]: round(float(prediction[0][1] * 100), 2),
            CLASS_NAMES[2]: round(float(prediction[0][2] * 100), 2),
        },
    }