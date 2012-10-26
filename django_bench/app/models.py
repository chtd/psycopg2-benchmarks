from django.db import models

class SomeModel(models.Model):
    name = models.CharField(max_length=255, blank=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
