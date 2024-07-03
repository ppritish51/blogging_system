from rest_framework import serializers
from .models import Course, CourseModule

# Course Serializers
class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'image_link', 'slug']

class CourseModuleIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModule
        fields = ['id', 'title', 'order']

class CourseDetailSerializer(serializers.ModelSerializer):
    modules = CourseModuleIndexSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'image_link', 'slug', 'modules']

class CourseModuleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModule
        fields = '__all__'