from django.db import models
from django.contrib.auth.models import User


class Badge(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='media')

    def __str__(self):
        return self.id


class Post(models.Model):
    class State(models.TextChoices):
        DRAFT = 'draft'
        RELEASE = 'release'

    title = models.CharField(max_length=100)
    content = models.TextField()
    state = models.CharField(choices=State.choices, max_length=100)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    release_date = models.DateTimeField()
    selected_image = models.ImageField(upload_to='media', blank=True)
    badges = models.ManyToManyField(Badge, related_name='blog_posts', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    images = models.ManyToManyField('Image', blank=True)

    def __str__(self):
        return self.title
