from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField


class Article(models.Model):
    title = models.CharField(max_length=150)
    summary = models.CharField(max_length=200, blank=True, default="")
    body = RichTextField()
    photo = models.ImageField(upload_to="images/", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    likes = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name="liked_articles",
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.pk)])

    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=150)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('article_list')
