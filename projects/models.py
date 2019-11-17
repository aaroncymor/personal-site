from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from tinymce import models as tinymce_models

from core.utils import (
    load_html_doc,
    get_html_content
)
from core.models import PortfolioMixin

# Create your models here.

class Project(PortfolioMixin):
    name = models.CharField(max_length=100)
    description = tinymce_models.HTMLField()
    rank = models.IntegerField(null=True)

    class Meta:
        db_table = 'project'

    @property
    def short_description_for_home(self):
        # Slice description to 200 characters
        return get_html_content(load_html_doc(self.description))[:200]

    @property
    def short_description_for_list(self):
        # Slice description to 200 characters
        return get_html_content(load_html_doc(self.description))[:500]

    def __str__(self):
        return self.name
