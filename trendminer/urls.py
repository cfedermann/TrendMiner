"""
Project: TrendMiner Demo Web Services
Authors: Christian Federmann <cfedermann@dfki.de>,
         Tim Krones <tkrones@coli.uni-saarland.de>
"""
from django.conf.urls.defaults import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'trendminer.views.home', name='home'),

    (r'^login/$', 'trendminer.views.login',
     {'template_name': 'login.html'}),

    (r'^logout/$', 'trendminer.views.logout',
     {'next_page': '/'}),

    url(r'^analyse/$', 'trendminer.views.analyse', name='analyse'),
    url(r'^analyse/(?P<request_id>\d{4}(-\d{2}){2}_(\d{2}-){2}\d{2}_.*)' \
            '/(?P<page>[1-9]\d*)/$',
        'trendminer.views.analyse', name='results'),

    # url(r'^trendminer/', include('trendminer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
