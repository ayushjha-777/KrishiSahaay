import os
from google import genai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PredictSerializer
from prediction.utils import image_to_numpy, is_leaf_image, calculate_severity


class HealthCheckView(APIView):
    def get(self, request):
        return Response(
            {
                "success": True,
                "message": "KrishiSahay Backend Running"
            },
            status=status.HTTP_200_OK
        )


class PredictAPIView(APIView):
    """
    Plant disease prediction API.
    Receives an image and returns the AI prediction.
    """

    def post(self, request):
        from prediction.services import predict_disease
        serializer = PredictSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Uploaded image
        image = serializer.validated_data["image"]

        # Reject images that don't look like plant leaves before
        # running them through the disease-prediction model.
        if not is_leaf_image(image):
            return Response(
                {"error": "Please upload a valid potato leaf image."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Convert to numpy array
        image_array = image_to_numpy(image)

        # AI prediction
        prediction = predict_disease(image_array)

        # Only diseased leaves have a meaningful "severity" -
        # a healthy leaf has no affected area to measure.
        severity = None
        if prediction["prediction"] != "Potato___healthy":
            severity = calculate_severity(image)

        return Response(
            {
                "success": True,
                "prediction": prediction,
                "severity": severity,
            },
            status=status.HTTP_200_OK
        )

class RecommendationAPIView(APIView):

    def post(self, request):
        try:
            disease = request.data.get("disease")
            confidence = request.data.get("confidence")
            severity_level = request.data.get("severity_level")
            severity_percent = request.data.get("severity_percent")

            lesion_area = request.data.get("lesion_area")
            lesion_count = request.data.get("lesion_count")
            avg_lesion_size = request.data.get("avg_lesion_size")
            color_score = request.data.get("color_score")
            distribution_score = request.data.get("distribution_score")

            # Basic validation
            if not disease:
                return Response(
                    {"error": "Disease is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            api_key = os.getenv("GEMINI_API_KEY")

            if not api_key:
                return Response(
                    {"error": "Gemini API key is not configured."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            client = genai.Client(api_key=api_key)

            prompt = f"""
You are the AI crop-care recommendation assistant for KrishiSahaay,
a potato disease detection application.

The disease diagnosis has already been made by our trained
MobileNetV2 disease-classification model.

IMPORTANT:
Do not change, question, or re-diagnose the supplied disease.

MODEL RESULT

Disease: {disease}
Model Confidence: {confidence}%

Disease Severity: {severity_level}
Severity Score: {severity_percent}%

MULTI-FACTOR LESION ANALYSIS

Affected Leaf Area: {lesion_area}%
Lesion Count: {lesion_count}
Average Lesion Size: {avg_lesion_size} pixels
Lesion Colour Severity: {color_score}%
Lesion Distribution Score: {distribution_score}%

Generate a concise and practical crop-management recommendation
for a potato farmer based on the supplied diagnosis and severity.

Return exactly these three sections:

IMMEDIATE ACTION:
Give the most important steps the farmer should take now.

DISEASE MANAGEMENT:
Explain how the detected disease should be managed.

PREVENTION:
Explain how future infection or spread can be reduced.

IMPORTANT SAFETY RULES:
- Keep the response concise and understandable.
- Prioritize cultural, sanitation and non-chemical management measures.
- Do not provide pesticide dosages.
- Do not recommend specific chemical products unless absolutely necessary.
- If chemical treatment may be required, advise the farmer to follow
  locally approved agricultural guidance and product labels.
- Do not contradict the supplied disease diagnosis.
"""

            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )

            recommendation = response.text

            return Response(
                {
                    "success": True,
                    "recommendation": recommendation
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print("Gemini recommendation error:", str(e))

            return Response(
                {
                    "success": False,
                    "error": "Unable to generate recommendation."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )