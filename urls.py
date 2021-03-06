from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('qofdb.views',
                       (url(r'^faq/', include('faq.urls'))),
                       (r'^browse/(?P<orgcode>\w{1,6})$','browse'),
                       (r'^browse/(?P<orgcode>\w{1,6})/(?P<year>\d{1,2})','browse'),
                       (r'^browse/(?P<orgcode>\w{1,6})/(?P<area>[\w ]+)/(?P<year>\d{1,2})','browse'),
                       (r'^child/(?P<orgcode>\w{1,6})/(?P<indicator>[\w ]+)$','area'),
                       (r'^child/(?P<orgcode>\w{1,6})/(?P<indicator>[\w ]+)/(?P<year>\d{1,2})$','area'),
                       (r'^timeline/(?P<orgcode>\w{1,6})/(?P<indicator>[\w ]+)$','timeline'),
                       (r'^search/$','search'),
                       (r'^surgery.php','translate'),
                       (r'^pct.php','translate'),
                       (r'^download','download'),
                       (r'^api/data/(?P<orgcode>\w{1,6})/(?P<year>\d{1,2})','api_all'),
                       (r'^api/children/(?P<orgcode>\w{1,6})/(?P<year>\d{1,2})','api_children'),
                       (r'^api/areas$','api_areas'),
                       (r'^api/timeline/(?P<orgcode>\w{1,6})/(?P<indicator>[\w ]+)$','api_timeline'),
                       (r'^api/indicator/(?P<search>[\w ]+)$','api_indicator'),
                       (r'^api/indicator','api_indicator'),
                       (r'^$','browse',{'orgcode':'UK'}),


                       (url(r'^admin/', include(admin.site.urls))),
                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),

                      # Example:
    # (r'^qof/', include('qof.foo.urls')),


)

urlpatterns += staticfiles_urlpatterns()
