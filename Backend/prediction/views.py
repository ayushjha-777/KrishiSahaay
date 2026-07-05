from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PredictSerializer
from prediction.services import predict_disease
from prediction.utils import image_to_numpy


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

        serializer = PredictSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Uploaded image
        image = serializer.validated_data["image"]

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