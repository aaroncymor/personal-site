from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from tinymce import models as tinymce_models

from .managers import PublishedPostManager
from myportfolio.core.utils import parse_html_content
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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    content = tinymce_models.HTMLField()
    published_date = models.DateTimeField(blank=True, null=True)

    objects = models.Manager()
    published_objects = PublishedPostManager()

    class Meta:
        db_table = 'post'
    
    @property
    def short_content_for_home(self):
        # Slice content to 200 characters
        parsed_content = parse_html_content(self.content)
        return parsed_content[:200]

    @property
    def short_content_for_list(self):
        # Slice content to 500 characters
        parsed_content = parse_html_content(self.content)
        return parsed_content[:500]
    
    @property
    def tags_obj(self):
        return list(self.tags.all().values('tag'))
    
    @property
    def is_published(self):
        
        if self.published_date:
            return True
        return False

    def __str__(self):
        return self.title


class Tag(PortfolioMixin):
    tag = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='tags')

    class Meta:
        db_table = 'tag'
        unique_together = ('tag', 'post')
    
    def __str__(self):
        return self.tag
