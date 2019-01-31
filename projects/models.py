from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from tinymce import models as tinymce_models

from myportfolio.core.models import PortfolioMixin

# Create your models here.

class Project(PortfolioMixin):
    name = models.CharField(max_length=100)
    description = tinymce_models.HTMLField()

    class Meta:
        db_table = 'project'
    
    def short_description(self):
        return self.description[:150]
    
    def __str__(self):
        return self.name
