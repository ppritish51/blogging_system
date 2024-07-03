from rest_framework import serializers
from .models import BlogPost

class RelatedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['title', 'description', 'image_link', 'slug']

class BlogPostSimpleSerializer(serializers.ModelSerializer):
    """
    A simplified serializer for showing only a few fields of the related blog posts.
    """
    class Meta:
        model = BlogPost
        fields = ['title', 'description', 'image_link', 'slug']

class BlogPostSerializer(serializers.ModelSerializer):
    previous_post_data = serializers.SerializerMethodField()
    next_post_data = serializers.SerializerMethodField()
    related_posts_data = RelatedPostSerializer(source='related_posts', many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = '__all__'

    def get_previous_post_data(self, obj):
        """
        Get the data of the previous blog post.
        """
        if obj.previous_post and obj.previous_post.is_published:
            return BlogPostSimpleSerializer(obj.previous_post).data
        return None

    def get_next_post_data(self, obj):
        """
        Get the data of the next blog post.
        """
        # Using related_name 'next_post' from the BlogPost model to fetch the next post.
        try:
            next_post = obj.next_post.get()
            if next_post.is_published:
                return BlogPostSimpleSerializer(next_post).data
        except BlogPost.DoesNotExist:
            pass
        return None
