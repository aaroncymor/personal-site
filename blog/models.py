from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from tinymce import models as tinymce_models

from .managers import PublishedPostManager
from myportfolio.core.utils import (
    load_html_doc,
    get_html_content,
    get_tags
)
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
        soup = load_html_doc(self.content)
        deciphers = soup.select('span.decipher')
        for decipher in deciphers:
            decipher.decompose()
        
        return soup.get_text()[:200]

    @property
    def short_content_for_list(self):
        # Slice content to 500 characters
        soup = load_html_doc(self.content)
        deciphers = soup.select('span.decipher')
        for decipher in deciphers:
            decipher.decompose()

        return soup.get_text()[:200]
    
    @property
    def sanitized_content(self):
        soup = load_html_doc(self.content)
        deciphers = soup.select('span.decipher')
        for decipher in deciphers:
            decipher_id = decipher.get('id', '')
            decipher_classes = decipher.get('class', [])

            # create anchor tag
            anchor_tag = soup.new_tag('a')
            if decipher_id:
                anchor_tag['id'] = decipher_id
                anchor_tag['href'] = '#modal-' + decipher_id
            anchor_tag['class'] = decipher_classes + ['tooltipped', 'modal-trigger']
            anchor_tag['data-position'] = "top"
            anchor_tag['data-tooltip'] = "Click me, and try to crack code to unlock secret message."
            
            # create icon tag lock_outline from materialize
            close_lock_icon = soup.new_tag('i')
            close_lock_icon['class'] = ["small", "material-icons",  decipher_id + "-lock"]
            close_lock_icon.string = "lock_outline"
            
            # append icon tag to anchor tag
            anchor_tag.append(close_lock_icon)

            # create icon tag lock_open
            open_lock_icon = soup.new_tag('i')
            open_lock_icon['class'] = ["small", "material-icons",  decipher_id + "-lock"]
            open_lock_icon['style'] = "display:none"
            open_lock_icon['id'] = decipher_id + '-unlock'
            open_lock_icon.string = "lock_open"

            decipher.insert_after(open_lock_icon)
            decipher.replace_with(anchor_tag)
        return soup.prettify(formatter="html5")
    
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


class Decipher(PortfolioMixin):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='deciphers')
    hidden_text = models.CharField(max_length=255)
    name = models.CharField(max_length=100, null=True, default='')
    challenge = tinymce_models.HTMLField()
    clue = models.TextField()
    code = models.CharField(max_length=20, null=True, blank=True, default='')