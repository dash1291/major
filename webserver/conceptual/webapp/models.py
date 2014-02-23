from django.db import models
from django.contrib.auth.models import User


class Website(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(null=True, max_length=100)
	url = models.URLField()


class Page(models.Model):
	name = models.CharField(null=True, max_length=100)
	url = models.URLField()
	website = models.ForeignKey(Website)
