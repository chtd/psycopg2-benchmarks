from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField()
    author = models.ForeignKey(User, null=True)
