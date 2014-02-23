from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import webapp.views as webapp
from api.urls import router



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'conceptual.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', webapp.home),
    url(r'^play/', webapp.play),
    url(r'^browse/', webapp.browse),
    url(r'^signup/', webapp.signup),
    url(r'^signin/', webapp.signin),
    url(r'^logout/', webapp.signout),


    url(r'^dashboard/$', webapp.dashboard),
    url(r'^dashboard/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'dashboard'})
)
