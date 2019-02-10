from django.db import models

class ProjectRankManager(models.Manager):
    def get_rank_choices(self):
        queryset = self.get_queryset()
        return tuple([(i, str(i)) for i in range(1, queryset.count() + 1)])