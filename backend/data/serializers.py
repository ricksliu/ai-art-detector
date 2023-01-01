from rest_framework import serializers

from .models import SampleImage


class SampleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleImage
        fields = '__all__'
