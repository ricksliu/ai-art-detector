from rest_framework import serializers

from .models import RequestImage


class RequestImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestImage
        fields = [
            'filename',
            'url',
            'timestamp',
            'is_ai_generated',
        ]
