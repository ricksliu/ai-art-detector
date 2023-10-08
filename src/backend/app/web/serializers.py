from rest_framework import serializers

from .models import WebImage


class WebImageSerializer(serializers.ModelSerializer):
    model_is_ai_generated = serializers.SerializerMethodField()

    class Meta:
        model = WebImage
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['model_version'] = self.context['model_version']
        representation['model_prediction'] = self.context['model_prediction']
        return representation

    def get_model_is_ai_generated(self, _):
        return self.context['model_prediction'] >= 0.5
