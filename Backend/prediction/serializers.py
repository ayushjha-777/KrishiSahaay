from rest_framework import serializers


class PredictSerializer(serializers.Serializer):
    image = serializers.ImageField(
        required=True,
        allow_empty_file=False,
        use_url=False,
    )