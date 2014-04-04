from hashlib import md5
import json
import os

from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from webapp.models import Website, Page
from conceptual.utils import process_url


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


    def post_save(self, obj, *args, **kwargs):
        import pdb; pdb.set_trace()
        extraction_file_path = process_url(self.object.url)
        self.object.extractions_file = extraction_file_path
        self.object.save()
        super(PageViewSet, self).post_save(obj, *args, **kwargs)


@api_view(['GET'])
def extractions(request):
    website_addr = request.GET.get('website')
    page_addr = request.GET.get('page')

    page = get_object_or_404(website_addr, page_addr)
    extractions = open(os.path.join(settings.EXTRACTIONS_PATH,
        page.extractions_file)).read()
    return Response(json.dumps(extractions))
