"""
Project: TrendMiner Demo Web Services
Authors: Christian Federmann <cfedermann@dfki.de>,
         Tim Krones <tkrones@coli.uni-saarland.de>
"""
from django.conf.urls.defaults import include, patterns, url

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

    url(r'^analyze/$', 'trendminer.views.analyze', name='analyze'),

    # url(r'^trendminer/', include('trendminer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
