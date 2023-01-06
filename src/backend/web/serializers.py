from rest_framework import serializers

from .models import WebImage


class WebImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebImage
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['model_version'] = self.context['model_version']
        representation['model_prediction'] = self.context['model_prediction']
        representation['model_is_ai_generated'] = self.context['model_is_ai_generated']
        return representation
