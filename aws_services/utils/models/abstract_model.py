from django.db import models
from django.utils import timezone


class CommonItems(models.Model):
    """
    This is abstract model and will be included with all other models
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True
