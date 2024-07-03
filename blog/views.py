from rest_framework import generics
from .models import BlogPost
from .serializers import BlogPostSerializer, BlogPostSimpleSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from .models import Course, CourseModule, Book, BookChapter
from .serializers_book import (
    BookListSerializer, BookDetailSerializer, BookChapterDetailSerializer
)

from .serializers_course import (
    CourseListSerializer, CourseDetailSerializer, CourseModuleDetailSerializer
)


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 15

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'results': data
        })


class BlogPostList(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = BlogPost.objects.filter(is_published=True, is_sub_page=False).order_by('-date_created').all()
    serializer_class = BlogPostSimpleSerializer
    pagination_class = CustomPageNumberPagination
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'blog'


class BlogPostDetail(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    queryset = BlogPost.objects.filter(is_published=True).all()
    serializer_class = BlogPostSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'blog'


# Course API Views
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]


class CourseModuleDetailView(generics.RetrieveAPIView):
    queryset = CourseModule.objects.all()
    serializer_class = CourseModuleDetailSerializer
    lookup_url_kwarg = "module_id"
    permission_classes = [IsAuthenticated]


# Book API Views
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]


class BookChapterDetailView(generics.RetrieveAPIView):
    queryset = BookChapter.objects.all()
    serializer_class = BookChapterDetailSerializer
    lookup_url_kwarg = "chapter_id"
    permission_classes = [IsAuthenticated]
