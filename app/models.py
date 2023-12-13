from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='static/media/', null=True, blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.pk)])

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.article

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.pk)])