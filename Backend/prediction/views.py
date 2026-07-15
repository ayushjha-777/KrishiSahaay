from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PredictSerializer
from prediction.utils import image_to_numpy, is_leaf_image


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

        return Response(
            {
                "success": True,
                "prediction": prediction
            },
            status=status.HTTP_200_OK
        )