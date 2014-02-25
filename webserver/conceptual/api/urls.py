from rest_framework import routers

from api.views import *


router = routers.DefaultRouter()
router.register(r'websites', WebsiteViewSet)
router.register(r'pages', PageViewSet)
