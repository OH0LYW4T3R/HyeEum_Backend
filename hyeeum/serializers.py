from .models import *
from rest_framework import serializers

class StatisticsSerializer(serializers.ModelSerializer): # ModelSerializer를 써야한다.
    class Meta:
        model = Statistics
        fields = "__all__"

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

class LibrarySerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    statistics = StatisticsSerializer(many=True, read_only=True)

    class Meta:
        model = Library
        fields = ['id', 'user_id', 'books', 'statistics', 'book_count']

class UserSerializer(serializers.ModelSerializer):
    librarys = LibrarySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'user_name', 'user_tag', 'created_at', 'birth', 'alignment', 'template', 'polite', 'librarys', 'library_count']