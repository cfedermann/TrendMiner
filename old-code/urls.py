"""
Django URLs configuration for the MUSING Service downloads application.

Defines the URLs for the MUSING Service CROWL section.

"""
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('reputation.views',
  (r'^rate_company/$', 'rate_company'),
  (r'^download/(?P<filename>\d{8})/$', 'download'),
)

# cfedermann: WSDL support disabled for post-MUSING deployment.
#
#urlpatterns += patterns('reputation.wsdl',
#  url(r'^$', 'REPUTATION_SERVICE', name='service'),
#  url(r'^services\.wsdl$', 'reputation_wsdl', name='wsdl'),
#)
