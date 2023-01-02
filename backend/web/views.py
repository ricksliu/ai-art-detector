from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import WebImageSerializer
from shared import utility
from django.conf import settings


class WebImageList(APIView):
    def post(self, request):
        image = utility.base64_to_image(request.data.get('image'))

        model_version = 'mock'
        model_target = '0.1234'
        model_is_ai_generated = False

        serializer = WebImageSerializer(data=request.data, context={
            'model_version': model_version,
            'model_target': model_target,
            'model_is_ai_generated': model_is_ai_generated,
        })
        if serializer.is_valid():
            serializer.save()
            image.save(settings.WEB_IMAGES_DIR / '{}.{}'.format(serializer.data.get('id'), request.data.get('type')))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
