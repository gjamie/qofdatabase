from django.conf.urls.defaults import *

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
                       (r'^$','browse',{'orgcode':'UK'}),

                       (url(r'^admin/', include(admin.site.urls))),
                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),

                      # Example:
    # (r'^qof/', include('qof.foo.urls')),


)
