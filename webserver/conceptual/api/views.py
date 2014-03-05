from hashlib import md5

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

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

    def get_serializer(self, instance=None, data=None,
                       files=None, many=False, partial=False):
        if self.action in ['update', 'create']:
            # Inject current user's id into the data so that its not required
            # in the request payload.
            data['user'] = self.request.user.id

        return super(WebsiteViewSet, self).get_serializer(instance, data,
                     files, many, partial)



class PageSerializer(ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'name', 'url')


class PageViewSet(viewsets.ModelViewSet):
    model = Page
    serializer = PageSerializer

    def get_queryset(self):
        return Page.objects.filter(website_id=self.kwargs['website_id'])

    def get_serializer(self, instance=None, data=None,
                       files=None, many=False, partial=False):
        if self.action in ['update', 'create']:
            # Inject the website's id into the data so that its not required
            # in the request payload.
            data['website'] = self.kwargs['website_id']

        return super(PageViewSet, self).get_serializer(instance, data,
                     files, many, partial)
