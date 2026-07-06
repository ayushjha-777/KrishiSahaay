
from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def validate_image(self, image):

        max_size = 5 * 1024 * 1024  # 5 MB

        if image.size > max_size:
            raise serializers.ValidationError(
                "Image size should be less than 5MB"
            )

        allowed = ['jpg', 'jpeg', 'png']

        ext = image.name.split('.')[-1].lower()

        if ext not in allowed:
            raise serializers.ValidationError(
                "Only JPG, JPEG and PNG allowed"
            )

        return image


class PredictSerializer(serializers.Serializer):
    image = serializers.ImageField(
        required=True,
        allow_empty_file=False,
        use_url=False,
    )