from django.urls import path
from .views import BlogPostList, BlogPostDetail
from .views import (
    CourseListView, CourseDetailView, CourseModuleDetailView,
    BookListView, BookDetailView, BookChapterDetailView
)

urlpatterns = [
    path('post/', BlogPostList.as_view(), name='blog-list'),
    path('post/<slug:slug>/', BlogPostDetail.as_view(), name='blog-detail'),

    # New URL patterns for Course
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<slug:slug>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/<slug:slug>/<int:module_id>/', CourseModuleDetailView.as_view(), name='course-module-detail'),

    # New URL patterns for Book
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<slug:slug>/', BookDetailView.as_view(), name='book-detail'),
    path('books/<slug:slug>/<int:chapter_id>/', BookChapterDetailView.as_view(), name='book-chapter-detail'),
]
