from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models import Book, Library, User, Statistics
from ..serializers import BookSerializer
from .user_views import copy_request_data
from ..GenerativeAI.gpt_api import getGPTAPI
from ..GenerativeAI.gpt_views import key_value

from PIL import Image
from io import BytesIO
import requests, os
from pathlib import Path
from django.core.files import File

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MEDIA_ROOT = MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

def generation(book_queryset, statistics_queryset):
    question = ""
    emotion = "기쁨 : " + str(statistics_queryset[0].happiness) + " 화남 : " + str(statistics_queryset[0].aggro) + " 슬픔 : " + str(statistics_queryset[0].sadness) + " 즐거움 : " + str(statistics_queryset[0].joy) + "\n"
    detail_story = ""
    day = 1

    for instance in book_queryset:
        detail_story += f"day {day}\n"

        detail_story += instance.detail_story
        detail_story += "\n\n"

        day += 1

    question = emotion + detail_story
    total_string = getGPTAPI(question, 4)

    result = key_value(total_string)
    print(result["Comment"])

    return result["Comment"]

def image_delete(usertag, library_id, string):
    str_list = string.split("/")
    filename = str_list[-1]

    path = os.path.join(MEDIA_ROOT, f"{usertag}")
    path = os.path.join(path, f"{library_id}")
    path = os.path.join(path, filename)

    print(path)

    if os.path.exists(path):
        os.remove(path)
    else: print("Not Delete")

def save_image_from_url(image_url, file_name):
    try:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))

        file_bytes_io = BytesIO()
        img.save(file_bytes_io, format='JPEG')
        
        file_bytes_io.seek(0)
        
        return File(file_bytes_io, name=file_name)
    except Exception as e:
        print("Error while saving image:", e)
        return None

# 책 최대 개수
MAX_BOOK_COUNT = 5

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    #생성
    def create(self, request, *args, **kwargs):
        library_queryset = Library.objects.filter(id=request.data.get("library_id"))
        
        if library_queryset.exists():
            if library_queryset[0].book_count == MAX_BOOK_COUNT:
                return Response({"Error : Max Book"}, status=status.HTTP_400_BAD_REQUEST)
        
            image = save_image_from_url(request.data.get("image"), "temp_image.jpg")
           
            if image != None:
                req_data = copy_request_data(request.data)
                req_data["image"] = image
                serializer = self.get_serializer(data=req_data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)

                book_count = library_queryset[0].book_count + 1
                library_queryset.update(book_count=book_count)

                library_instance = library_queryset[0]

                statistics_queryset = Statistics.objects.filter(library_id=request.data.get("library_id"))
                emotion = request.data.get("emotion")
                if emotion == "기쁨":
                    happiness = statistics_queryset[0].happiness + 1
                    statistics_queryset.update(happiness=happiness)
                elif emotion == "화남":
                    aggro = statistics_queryset[0].aggro + 1
                    statistics_queryset.update(aggro=aggro)
                elif emotion == "슬픔":
                    sadness = statistics_queryset[0].sadness + 1
                    statistics_queryset.update(sadness = sadness)
                elif emotion == "즐거움":
                    joy = statistics_queryset[0].joy + 1
                    statistics_queryset.update(joy=joy)

                if library_instance.book_count == MAX_BOOK_COUNT:
                    has_larger = Library.objects.filter(id__gt=library_instance.id)

                    # 제일 최근에 만들어진 것이 3개가 다 채워졌을때 생성
                    if not has_larger:
                        # GPT-Comment 생성
                        book_queryset = Book.objects.filter(library_id=library_instance.id)
                        statistics_queryset = Statistics.objects.filter(library_id=library_instance.id)
                        result = generation(book_queryset, statistics_queryset)

                        if statistics_queryset.exists():
                            statistics_queryset.update(gpt_comment=result)

                        # Create Library 
                        create_library = Library.objects.create(user_id=library_instance.user_id)
                        user_queryset = User.objects.filter(id=library_instance.user_id.id)
                        library_count = user_queryset[0].library_count + 1
                        user_queryset.update(library_count=library_count)

                        # Create Statistics
                        Statistics.objects.create(library_id=create_library)

                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                return Response({"Error : Image Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Error : Not Found Library"}, status=status.HTTP_404_NOT_FOUND)
        
    #수정    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        try :
            if "image" in request.data:
                req_data = copy_request_data(request.data)
                path = os.path.join(MEDIA_ROOT, str(instance.image).replace("/","\\"))
                os.remove(path=path)
                req_data["image"] = save_image_from_url(request.data.get("image"), "temp_image.jpg")
                serializer = self.get_serializer(instance, data=req_data, partial=partial)
            else: serializer = self.get_serializer(instance, data=request.data, partial=partial)
            
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response({"Success : Change"}, status=status.HTTP_200_OK)
        
        except:
            return Response({"Error : Original Image Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
    #삭제
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        library_instance = Library.objects.filter(id=instance.library_id.id)
        book_count = library_instance[0].book_count
        if book_count > 0: library_instance.update(book_count=book_count-1)

        statistics_queryset = Statistics.objects.filter(library_id=library_instance[0].id)
        emotion = str(Book.objects.filter(id=kwargs.get("pk"))[0].emotion)

        image_delete(instance.library_id.user_id.user_tag, instance.library_id.id, str(instance.image))

        self.perform_destroy(instance)

        if emotion == "기쁨":
            happiness = statistics_queryset[0].happiness
            if happiness > 0: statistics_queryset.update(happiness=happiness-1)
        elif emotion == "화남":
            aggro = statistics_queryset[0].aggro
            if aggro > 0: statistics_queryset.update(aggro=aggro-1)
        elif emotion == "슬픔":
            sadness = statistics_queryset[0].sadness
            if sadness > 0: statistics_queryset.update(sadness=sadness-1)
        elif emotion == "즐거움":
            joy = statistics_queryset[0].joy
            if joy > 0: statistics_queryset.update(joy=joy-1)
        return Response(status=status.HTTP_204_NO_CONTENT)