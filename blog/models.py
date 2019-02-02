from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from tinymce import models as tinymce_models

from myportfolio.core.models import PortfolioMixin

# Create your models here.

class Category(PortfolioMixin):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name


class Post(PortfolioMixin):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = tinymce_models.HTMLField()
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'post'
    
    @property
    def short_content(self):
        # Slice content to 150 characters
        return self.content[:150]
    
    @property
    def tags(self):
        return self.tag_set.all()[:4]
    
    def is_published(self):
        
        if self.published_date:
            return True
        return False
    
    def get_category(self):
        return self.category.name
    
    def get_tags(self):
        tags = Tag.objects.filter(post__id=self.id).values_list('name', flat=True)
        return tags

    def __str__(self):
        return self.title


class Tag(PortfolioMixin):
    name = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tag'
        unique_together = ('name', 'post')
    
    def __str__(self):
        return self.name
