from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import WebImageSerializer
from shared.utility import base64_to_pil_image
from data import predict

from django.conf import settings


class WebImageList(APIView):
    def post(self, request):
        """
        Return the model's prediction for a posted image.
        """

        # Predict image
        image = base64_to_pil_image(request.data.get('image'))
        prediction = predict.predict_is_ai_generated(image)

        # Serialize image with context
        context = {
            'model_version': settings.MODEL_VER,
            'model_prediction': prediction,
        }
        serializer = WebImageSerializer(data=request.data, context=context)

        if serializer.is_valid():
            serializer.save(**context)  # Save instance with context
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
