from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_link = models.URLField(blank=True, null=True)
    body = RichTextField(blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True)
    publish_date = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    related_posts = models.ManyToManyField('self', blank=True)
    previous_post = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='next_post')

    is_sub_page = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def clean(self):
        # Check if the selected previous_post is already set as a previous_post for another blog
        if self.previous_post and BlogPost.objects.filter(previous_post=self.previous_post).exclude(
                id=self.id).exists():
            raise ValidationError(
                f"The post '{self.previous_post.title}' is already set as a previous post for another blog.")


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_link = models.URLField(blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_courses')
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True)
    publish_date = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    duration = models.DurationField()  # Duration of the entire course

    def __str__(self):
        return self.title


class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)
    order = models.PositiveIntegerField()  # to keep track of sequence
    content = RichTextField(blank=True, null=True)  # for module content

    class Meta:
        unique_together = ('course', 'order')  # Ensuring modules have unique order within a course

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_link = models.URLField(blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='written_books')
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True)
    publish_date = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    ISBN = models.CharField(max_length=13, unique=True)
    publisher = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class BookChapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=255)
    content = RichTextField(blank=True, null=True)
    order = models.PositiveIntegerField()  # to keep track of sequence

    class Meta:
        unique_together = ('book', 'order')  # Ensuring chapters have unique order within a book

    def __str__(self):
        return f"{self.book.title} - {self.title}"
