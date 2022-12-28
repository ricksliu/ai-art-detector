from rest_framework import serializers

from .models import SampleImage


class SampleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleImage
        fields = [
            'filename',
            'timestamp',
            'src',
            'src_id',
            'src_url',
            'src_timestamp',
            'is_ai_generated',
        ]
