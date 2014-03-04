from django.db import models
from django.contrib.auth.models import User


class Website(models.Model):
    user = models.ForeignKey(User, related_name='websites')
    name = models.CharField(null=True, max_length=100, unique=True)
    url = models.CharField(unique=True, max_length=200)
    embed_src = models.CharField(max_length=200, blank=True)


class Page(models.Model):
    name = models.CharField(null=True, max_length=100)
    url = models.CharField(max_length=200)
    website = models.ForeignKey(Website, related_name='pages')
