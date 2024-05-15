from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .dalle_api import getDALLE

@api_view(['POST'])
def image_generation(request):
    qna_string = request.data.get("qna_string")
    emotion = request.data.get("emotion")
    result = {"image_url" : getDALLE(qna_string, emotion=emotion)}

    return Response(result, status=status.HTTP_200_OK)