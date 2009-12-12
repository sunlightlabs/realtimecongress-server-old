from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('realtimecongress_server.api.urls_api')),
    url(r'^feeds/', include('realtimecongress_server.api.urls_feeds')),
)
