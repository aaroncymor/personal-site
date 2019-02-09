from django.db import models

class PublishedPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset() \
            .filter(published_date__isnull=False) \
            .order_by('-timestamp')