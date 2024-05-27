from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .gpt_api import getGPTAPI

def key_value(string):
        lines = string.split('\n')
        
        # 결과를 저장할 딕셔너리
        result = {}
        
        for line in lines:
            # 각 줄에서 ':'를 기준으로 분리
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # nickname의 경우 공백을 기준으로 나누어 리스트로 변환
            if key == 'nickname':
                value = value.split()
            
            result[key] = value

        return result

@api_view(['POST'])
def nickname_generation(request):
    qna_string = request.data.get("qna_string")
    result = key_value(getGPTAPI(qna_string, 1))

    return Response(result, status=status.HTTP_200_OK)

@api_view(['POST'])
def question_generation(request):
    qna_string = request.data.get("qna_string")
    alignment = request.data.get("alignment")
    polite = request.data.get("polite")
    result = {"question" : getGPTAPI(qna_string, 2, alignment=alignment)}

    return Response(result, status=status.HTTP_200_OK)

@api_view(['POST'])
def emotion_generation(request):
    qna_string = request.data.get("qna_string")
    alignment = request.data.get("alignment")
    polite = request.data.get("polite")
    result = key_value(getGPTAPI(qna_string, 3, alignment=alignment))

    return Response(result, status=status.HTTP_200_OK)

