from django.conf.urls import include, patterns, url

from rest_framework import routers

from api.views import *


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'websites', WebsiteViewSet)
router.register(r'websites/(?P<website_id>\d+)/pages', PageViewSet)


api_urls = patterns('',
    url(r'', include(router.urls)),
    url(r'profile/', profile, name='api-profile'),
    url(r'websites/(?P<website_id>\d+)/embed', embed, name='api-embed')
)
