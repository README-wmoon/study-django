from django.db import models
from django.utils import timezone


class Period(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True