from django.shortcuts import render
from rest_framework.views import APIView#APIView is a class-based view that provides the basic functionality for handling HTTP requests in Django REST framework. It allows you to define methods for different HTTP verbs (GET, POST, PUT, DELETE, etc.) and handle the request data accordingly.isiki madad se hm restapi bnate hai,APIView  django rest framework ka ek class hai jo ki api banane me help karta hai, isme hm http method jaise get,post,put,delete method define kar sakte hai
from rest_framework.response import Response#ye json Response bhejne ke liye use hota hai, ye django rest framework ka ek class hai jo ki json response bhejne me help karta hai
from rest_framework import status#HTTP status codes ke liye.
from .serializers import PredictSerializer#ye serializer ka use data ko validate karne ke liye hota hai, jaise ki image data ko validate karne ke liye.

#Jaise:

#HTTP_200_OK → Success
#HTTP_400_BAD_REQUEST → Client error
#HTTP_404_NOT_FOUND → Not found
#HTTP_500_INTERNAL_SERVER_ERROR → Server error
class predictAPIView(APIView):
    def post(self, request):#yha jo request part hai yha har type ka data aa sakta hai jaise ki json, form data, file data ,image etc. 
        return Response({"success": True, "message": "Prediction successful"}, status=status.HTTP_200_OK)
        # Get the input data from the request
# Create your views here.

    
        serializer = PredictSerializer(data=request.data)
        if serializer.is_valid():
            # Perform prediction logic here
            # For demonstration purposes, we'll just return a success message
            return Response({"success": True, "message": "Prediction successful"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
