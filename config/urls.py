"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from hyeeum.views.user_views import UserViewSet
from hyeeum.views.library_views import LibraryViewSet
from hyeeum.views.book_views import BookViewSet
from hyeeum.views.statistics_views import StatisticsViewSet
from hyeeum.GenerativeAI.gpt_views import *
from hyeeum.GenerativeAI.dalle_views import *

from django.views.static import serve
from django.urls import re_path
from django.conf import settings

class OptionalSlashRouter(DefaultRouter): # trailing slash remove
    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'

router = OptionalSlashRouter()
router.register(r'users', UserViewSet)
router.register(r'library', LibraryViewSet)
router.register(r'books', BookViewSet)
router.register(r'statistics', StatisticsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('/', include(router.urls)),
    path('nickname', nickname_generation, name="nickname_generation_endpoint"),
    path('question-generation', question_generation, name="question_generation_endpoint"),
    path('emotion-generation', emotion_generation, name="emotion_generation_endpoint"),
    path('image-generation', image_generation, name="image_generation_endpoint"),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
]

urlpatterns += router.urls
