from django.db import models
from django.contrib.auth.models import User


class Website(models.Model):
    user = models.ForeignKey(User, related_name='websites')
    name = models.CharField(null=True, max_length=100, unique=True)
    url = models.CharField(unique=True, max_length=200, db_index=True)
    embed_src = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        pages = self.pages.all()

        for page in pages:
            relative_url = page.url[page.url.find('/'):]
            page.url = self.url + relative_url
            page.save()

        super(Website, self).save(*args, **kwargs)


class Page(models.Model):
    name = models.CharField(null=True, max_length=100)
    url = models.CharField(max_length=200, db_index=True)
    website = models.ForeignKey(Website, related_name='pages')
    extractions_file = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        relative_url = self.url[self.url.find('/'):]
        self.url = self.website.url + relative_url
        super(Page, self).save(*args, **kwargs)
