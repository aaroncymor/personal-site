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
    
    def is_published(self):
        
        if self.published_date:
            return True
        return False
    
    def get_category(self):
        return self.category.name
    
    def get_tags(self):
        tags = Tag.objects.filter(post__id=self.id).value_list('name', flat=True)
        return tags

    def __str__(self):
        return self.title


class Tag(PortfolioMixin):
    name = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tag'
        unique_together = ('name', 'post')
