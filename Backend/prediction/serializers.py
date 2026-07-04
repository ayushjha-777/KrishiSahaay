from rest_framework import serializers#serializers ka use data ko serialize karne ke liye hota hai, jaise ki json data ko python object me convert karna ya python object ko json data me convert karna.seializers data check karne wale tools rkhta hai.
class PredictSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True, allow_empty_file=False, use_url=False)
    #image field ka use image data ko validate karne ke liye hota hai,
