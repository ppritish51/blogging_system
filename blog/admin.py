from django.contrib import admin
from django.forms import ModelForm, ModelMultipleChoiceField
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import BlogPost
from .models import Course, CourseModule, Book, BookChapter
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import messages
from django.db import models


#####################################################################################
class BlogPostForm(ModelForm):
    related_posts = ModelMultipleChoiceField(
        queryset=BlogPost.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Related Posts',
            is_stacked=False
        )
    )

    class Meta:
        model = BlogPost
        fields = '__all__'

class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostForm
    prepopulated_fields = {'slug': ('title',), }
    list_display = ('title', 'author', 'date_created', 'is_published')
    search_fields = ('title', 'description')
    autocomplete_fields = ['previous_post', 'related_posts', 'author']

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)


#####################################################################################
class CourseModuleInline(admin.TabularInline):
    model = CourseModule
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget()},  # Use CKEditor for TextFields in inline
    }

class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_created', 'is_published', 'author']
    list_filter = ['is_published', 'date_created']
    search_fields = ['title', 'description']
    inlines = [CourseModuleInline]
    prepopulated_fields = {"slug": ("title",)}
    
    # A custom save_model function to catch any ValidationError and display them as messages in the admin
    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)


#####################################################################################
class BookChapterInline(admin.TabularInline):
    model = BookChapter
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget()},  # Use CKEditor for TextFields in inline
    }

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_created', 'is_published', 'author', 'ISBN']
    list_filter = ['is_published', 'date_created']
    search_fields = ['title', 'description', 'ISBN']
    inlines = [BookChapterInline]
    prepopulated_fields = {"slug": ("title",)}

    # A custom save_model function to catch any ValidationError and display them as messages in the admin
    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)

#####################################################################################


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Book, BookAdmin)
