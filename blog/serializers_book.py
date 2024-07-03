from rest_framework import serializers
from .models import Book, BookChapter

# Book Serializers
class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'image_link', 'slug']

class BookChapterIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookChapter
        fields = ['id', 'title', 'order']

class BookDetailSerializer(serializers.ModelSerializer):
    chapters = BookChapterIndexSerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'image_link', 'slug', 'chapters']

class BookChapterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookChapter
        fields = '__all__'
