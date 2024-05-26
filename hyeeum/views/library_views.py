from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models import Library, User
from ..serializers import LibrarySerializer

from pathlib import Path
import os, shutil

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MEDIA_ROOT = MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

def delete_directory(user_id, library_id):
    directory = os.path.join(MEDIA_ROOT, str(user_id))
    directory = os.path.join(directory, str(library_id))
    try:
        shutil.rmtree(directory)
        print(f"{directory} 및 하위에 있는 모든 파일 및 디렉토리를 삭제했습니다.")
    except Exception as e:
        print(f"디렉토리 삭제 중 오류 발생: {e}")

class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

    def list(self, request, *args, **kwargs):
        instance = User.objects.filter(user_tag=request.query_params.get('user_tag'))

        if instance.exists(): 
            queryset = Library.objects.filter(user_id=instance[0].id)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else: return Response({"Error : Not Found Tag"}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        user_instance = User.objects.filter(user_tag=request.data.get('user_tag'))

        if user_instance.exists():
            instance = Library.objects.filter(user_id=user_instance[0].id, id=kwargs.get("pk"))
            if instance.exists():
                serializer = self.get_serializer(instance[0])
                return Response(serializer.data)
        
        return Response({"Error : Not Found Tag or Library"}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
    
        user_instance = User.objects.filter(id=instance.user_id.id)
        library_count = user_instance[0].library_count
        if library_count > 0: user_instance.update(library_count=library_count-1)

        delete_directory(instance.user_id.id, instance.id)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
        