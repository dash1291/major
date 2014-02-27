from hashlib import md5

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from webapp.models import Website, Page


def get_gravatar_url(email):
	email_hash = md5(email).hexdigest()
	return 'http://www.gravatar.com/avatar/%s?s=32' % email_hash


@api_view(['GET'])
def profile(request):
	return Response({
		'email': request.user.email,
		'picture': get_gravatar_url(request.user.email)
	})


class WebsiteViewSet(viewsets.ModelViewSet):
    model = Website

    def get_queryset(self):
    	return Website.objects.filter(user_id=self.request.user.id)


class PageViewSet(viewsets.ModelViewSet):
    model = Page

    def get_queryset(self):
    	return Page.objects.filter(website_id=self.website_id)
