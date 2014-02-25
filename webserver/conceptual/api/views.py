from webapp.models import Website, Page

from rest_framework import viewsets, routers

# ViewSets define the view behavior.
class WebsiteViewSet(viewsets.ModelViewSet):
    model = Website

class PageViewSet(viewsets.ModelViewSet):
    model = Page
