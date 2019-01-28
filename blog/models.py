from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from tinymce import models as tinymce_models

# Create your models here.
class PortfolioMixin(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Category(PortfolioMixin):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'category'


class Post(PortfolioMixin):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = tinymce_models.HTMLField()
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'post'


class Tag(PortfolioMixin):
    name = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tag'
        unique_together = ('id', 'post')
