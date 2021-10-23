from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
import os
def upload_by_name(instance, filename):
    return f"{instance.name}{os.path.splitext(filename)[1]}"
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')
    pass
class Post(models.Model):
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()
    STATUS_CHOICES = (
        ('draft',"Draft"),
        ('published','Published'),
    )
    bgimg = models.ImageField(upload_to='assets/%Y/%m/%d',blank=True)
    title = models.CharField(
        max_length=250)
    subtitle = models.CharField(max_length=250, blank=True, null=True)
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name = 'blog_posts'
        )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices = STATUS_CHOICES,
        default='draft'
    )
    class Meta:
        ordering = ("-publish",)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('blog_app:post_detail',args=[self.pk])
class BlogImage(models.Model):
    name = models.CharField(max_length=80)
    image = models.ImageField(upload_to=upload_by_name)
    blog = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    pass
class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
