import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PredictSerializer
from prediction.services import predict_disease
from prediction.utils import image_to_numpy

# ye logger ka use hum error handling ke liye karenge. jaise ki agar model load nahi hua ya prediction mein koi error aaya to usko log karna hoga. iske liye hum try-except block use karenge.
# Yeh  Internal Black Box Recoder hai. Jab server live hota hai aur background mein koi error aata, toh yeh use hamare terminal ya ek log file mein print/save kar deta hai taaki aap baad mein dekh sako ki backend kyun crash hua tha.
logger = logging.getLogger(__name__)

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
        # serializer check kar raha hai ki jo data humne post request mein bheja hai wo valid hai ya nahi. agar valid nahi hai to ye serializer error throw kar dega aur humne upar isko handle kar liya hai
        serializer = PredictSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Uploaded image
        # ye part exception handling khud kar leta hai kyuki ye serializer ke through aa rha hai. agar image valid nahi hai to ye serializer error throw kar dega aur humne upar isko handle kar liya hai. ab humko bas image ko numpy array mein convert karna hai aur fir model ko call karna hai.
        image = serializer.validated_data["image"] 
        
        try:
            # Step A: Convert to numpy array
            image_array = image_to_numpy(image)

            # Step B: AI prediction
            prediction = predict_disease(image_array)

            # Step C: Success response
            return Response(
                {
                    "success": True,
                    "message": "Prediction successful",
                    "prediction": prediction,#yha pe jo ""mein likha hai wo data store kr rha hai jo ki prediction k pass hai aur yha prediction mein confidence ,probablities ,aur prediction sb ek mein hai.
                },
                status=status.HTTP_200_OK,
            )
            
        except ValueError as val_err:
            logger.error(f"Image preprocessing dimensions mismatch: {val_err}")
            return Response(
                {
                    "success": False,
                    "message": "Invalid image dimensions for the ML model."
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
            
        except Exception as ml_err:
            logger.error(f"Critical ML Pipeline Error: {str(ml_err)}")
            return Response(
                {
                    "success": False,
                    "message": "AI model failed to process the request.",
                    "error_details": str(ml_err)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )