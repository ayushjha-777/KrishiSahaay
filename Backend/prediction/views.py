import os
import json

from google import genai

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PredictSerializer
from prediction.utils import (
    image_to_numpy,
    is_leaf_image,
    calculate_severity,
)


class HealthCheckView(APIView):
    def get(self, request):
        return Response(
            {
                "success": True,
                "message": "KrishiSahay Backend Running",
            },
            status=status.HTTP_200_OK,
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
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Uploaded image
        image = serializer.validated_data["image"]

        # Reject images that don't look like plant leaves before
        # running them through the disease-prediction model.
        if not is_leaf_image(image):
            return Response(
                {
                    "error": "Please upload a valid potato leaf image."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Convert image to numpy array
        image_array = image_to_numpy(image)

        # AI disease prediction
        prediction = predict_disease(image_array)

        # Healthy leaves do not require severity analysis.
        severity = None

        if prediction["prediction"] != "Potato___healthy":
            severity = calculate_severity(image)

        return Response(
            {
                "success": True,
                "prediction": prediction,
                "severity": severity,
            },
            status=status.HTTP_200_OK,
        )


class RecommendationAPIView(APIView):
    """
    Generates structured crop-care recommendations using Gemini
    based on the disease prediction and severity analysis.
    """

    def post(self, request):
        try:
            # -------------------------------------------------
            # Get prediction/severity information from frontend
            # -------------------------------------------------

            disease = request.data.get("disease")
            confidence = request.data.get("confidence")

            severity_level = request.data.get("severity_level")
            severity_percent = request.data.get("severity_percent")

            lesion_area = request.data.get("lesion_area")
            lesion_count = request.data.get("lesion_count")
            avg_lesion_size = request.data.get("avg_lesion_size")
            color_score = request.data.get("color_score")
            distribution_score = request.data.get(
                "distribution_score"
            )

            # -------------------------------------------------
            # Basic validation
            # -------------------------------------------------

            if not disease:
                return Response(
                    {
                        "success": False,
                        "error": "Disease is required.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # -------------------------------------------------
            # Gemini API configuration
            # -------------------------------------------------

            api_key = os.getenv("GEMINI_API_KEY")

            if not api_key:
                return Response(
                    {
                        "success": False,
                        "error": "Gemini API key is not configured.",
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            client = genai.Client(api_key=api_key)

            # -------------------------------------------------
            # Gemini prompt
            # -------------------------------------------------

            prompt = f"""
You are the AI crop-care recommendation assistant for KrishiSahaay,
a potato disease detection application.

The disease diagnosis has already been made by our trained
disease-classification model.

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

TASK

Generate concise, practical, farmer-friendly crop-care
recommendations based on the supplied disease diagnosis and
severity information.

The recommendations should be appropriate for the detected
condition and its severity.

Return ONLY valid JSON using EXACTLY the following structure:

{{
    "immediate_action": [
        {{
            "title": "Short action title",
            "description": "Clear practical explanation of what the farmer should do."
        }}
    ],
    "disease_management": [
        {{
            "title": "Short management title",
            "description": "Clear practical explanation of how the condition should be managed."
        }}
    ],
    "prevention": [
        {{
            "title": "Short prevention title",
            "description": "Clear practical explanation of how future infection or spread can be reduced."
        }}
    ]
}}

STRICT RESPONSE RULES:

- Return ONLY the JSON object.
- Do not include Markdown.
- Do not use asterisks.
- Do not use bullet symbols.
- Do not use numbered lists.
- Do not include headings outside the JSON.
- Do not add explanatory text before the JSON.
- Do not add explanatory text after the JSON.
- Every recommendation must contain a title and description.
- Give 2 to 4 useful recommendations in each section.
- Keep titles short and meaningful.
- Keep descriptions concise and easy to understand.
- Avoid unnecessary technical terminology.
- Make recommendations relevant to the supplied severity.
- Prioritize cultural, sanitation and non-chemical management measures.
- Do not provide pesticide dosages.
- Do not recommend specific chemical products unless absolutely necessary.
- If chemical treatment may be required, advise the farmer to follow
  locally approved agricultural guidance and product labels.
- Do not contradict the supplied disease diagnosis.
"""

            # -------------------------------------------------
            # Generate recommendation
            # -------------------------------------------------

            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt,
            )

            if not response.text:
                return Response(
                    {
                        "success": False,
                        "error": "Gemini returned an empty response.",
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            raw_text = response.text.strip()

            # -------------------------------------------------
            # Remove accidental Markdown code fences
            # -------------------------------------------------

            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]

            elif raw_text.startswith("```"):
                raw_text = raw_text[3:]

            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]

            raw_text = raw_text.strip()

            # -------------------------------------------------
            # Convert Gemini JSON string into Python dictionary
            # -------------------------------------------------

            recommendation = json.loads(raw_text)

            # -------------------------------------------------
            # Validate expected structure
            # -------------------------------------------------

            required_sections = [
                "immediate_action",
                "disease_management",
                "prevention",
            ]

            for section in required_sections:
                if section not in recommendation:
                    raise ValueError(
                        f"Missing recommendation section: {section}"
                    )

                if not isinstance(recommendation[section], list):
                    raise ValueError(
                        f"Invalid recommendation section: {section}"
                    )

            # -------------------------------------------------
            # Return structured recommendation
            # -------------------------------------------------

            return Response(
                {
                    "success": True,
                    "recommendation": recommendation,
                },
                status=status.HTTP_200_OK,
            )

        except json.JSONDecodeError as e:
            print(
                "Gemini JSON parsing error:",
                str(e),
            )

            return Response(
                {
                    "success": False,
                    "error": "Unable to format recommendation.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as e:
            print(
                "Gemini recommendation error:",
                str(e),
            )

            return Response(
                {
                    "success": False,
                    "error": "Unable to generate recommendation.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )