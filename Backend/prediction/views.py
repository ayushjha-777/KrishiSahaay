# APIView ek class-based view hai jo Django REST Framework me REST API banane ke liye use hoti hai.
# Isme hum GET, POST, PUT, DELETE jaise HTTP methods define kar sakte hain.
from rest_framework.views import APIView

# Response JSON response bhejne ke liye use hota hai.
# Ye Python dictionary ko automatically JSON me convert kar deta hai.
from rest_framework.response import Response

# HTTP status codes (200, 400, 404, 500...) ko readable banane ke liye.
from rest_framework import status

# Serializer client se aaye hue data ko validate karega.
# Jaise image aayi ya nahi, image valid hai ya nahi.
from .serializers import PredictSerializer


class PredictAPIView(APIView):
    """
    Plant disease prediction API.
    Ye API React Native se image receive karegi aur
    future me ML model se prediction return karegi.
    """

    # React Native image ko POST request ke through bhejega.
    # request object ke andar client ka sara data hota hai.
    # request.data me JSON, Form Data, Image, File etc. aa sakta hai.
    def post(self, request):

        # Client se aaye hue data ko serializer ke paas bhej rahe hain.
        # Serializer request data ko validate karega.
        serializer = PredictSerializer(data=request.data)

        # Agar data valid nahi hai to error return kar do.
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validation ke baad safe data validated_data me milta hai.
        # Ab request.data ki jagah validated_data use karna best practice hai.
        image = serializer.validated_data["image"]

        # Yahan future me TensorFlow MobileNetV2 model ko image bhejenge.
        # prediction = predict_disease(image)

        # Abhi sirf testing ke liye success response bhej rahe hain.
        return Response(
            {
                "success": True,
                "message": "Prediction successful",
                "data":{},
            },
            status=status.HTTP_200_OK
        )