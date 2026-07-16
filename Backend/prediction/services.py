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
    "potato_disease_model.tflite"
)


class ModelLoader:
    _interpreter = None
    _input_details = None
    _output_details = None

    @classmethod
    def get_interpreter(cls):
        if cls._interpreter is None:
            # ai-edge-litert is a lightweight TFLite-only runtime.
            # Unlike full TensorFlow, importing it takes a fraction of a
            # second and uses a fraction of the memory, which is essential
            # on resource-constrained hosts like Render's free tier.
            from ai_edge_litert.interpreter import Interpreter

            logger.info("Loading AI model (TFLite)...")
            interpreter = Interpreter(model_path=MODEL_PATH)
            interpreter.allocate_tensors()

            cls._interpreter = interpreter
            cls._input_details = interpreter.get_input_details()
            cls._output_details = interpreter.get_output_details()
            logger.info("Model loaded successfully.")

        return cls._interpreter, cls._input_details, cls._output_details


def predict_disease(image_array):

    interpreter, input_details, output_details = ModelLoader.get_interpreter()

    image_array = image_array.astype(np.float32)

    interpreter.set_tensor(input_details[0]["index"], image_array)
    interpreter.invoke()
    prediction = interpreter.get_tensor(output_details[0]["index"])

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
