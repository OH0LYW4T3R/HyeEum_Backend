from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models import User, Library
from ..serializers import UserSerializer
# Create your views here.

def copy_request_data(data):
    req_data = {}

    print(data)
    for key, value in data.items():
        req_data[key] = value

    return req_data

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # 생성
    def create(self, request, *args, **kwargs):
        tag_id = 1
        req_data = copy_request_data(request.data)
        
        # Create User Tag
        end_user = self.get_queryset().last()
        if end_user is not None: 
            tag_id = end_user.id + 1
            req_data['user_tag'] = tag_id
        else: req_data["user_tag"] = 1
        
        serializer = self.get_serializer(data=req_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Create Library
        instance = User.objects.filter(user_tag=tag_id)
        if instance.exists(): 
            Library.objects.create(user_id=instance[0])
            library_count = instance[0].library_count + 1
            instance.update(library_count=library_count)
        else: Response({"Error : Not Found Tag"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"Success : Create User"}, status=status.HTTP_201_CREATED, headers=headers)
    
    # 세부 조회
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    # 수정
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = User.objects.filter(user_tag=kwargs.get("pk"))[0]

        if "user_tag" not in request.data:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response({"Success : Change User"}, status=status.HTTP_200_OK)
        else:
            return Response({"Error : Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)