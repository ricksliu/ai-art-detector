from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from decimal import Decimal

from .serializers import WebImageSerializer
from shared import utility
from data import predict
from django.conf import settings


class WebImageList(APIView):
    def post(self, request):
        image = utility.base64_to_pil_image(request.data.get('image'))
        prediction = predict.predict_is_ai_generated(image)
        context = {
            'model_version': settings.MODEL_VER,
            'model_prediction': prediction,
            'model_is_ai_generated': prediction >= 0.5,
        }

        serializer = WebImageSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save(**context)
            image.save(settings.WEB_IMAGES_DIR + '{}.{}'.format(serializer.data.get('id'), request.data.get('type')))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
