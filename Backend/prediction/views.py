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
            print(serializer.errors)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validation ke baad safe data validated_data me milta hai.
        # Ab request.data ki jagah validated_data use karna best practice hai.
        image = serializer.validated_data["image"]

        image_array = image_to_numpy(image)
        
        prediction = predict_disease(image_array)

        # Abhi sirf testing ke liye success response bhej rahe hain.
        return Response(
            {
                "success": True,
                "prediction": prediction, 
            },
            status=status.HTTP_200_OK
        )
