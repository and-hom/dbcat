from django.conf.urls import patterns, url

from frontend.views import index, db, boolean_filter, int_range_filter, select_filter, about

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'dbcat.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^$', index),
                       url(r'^boolean_filter$', boolean_filter),
                       url(r'^int_range_filter$', int_range_filter),
                       url(r'^select_filter$', select_filter),
                       url(r'^db$', db),
                       url(r'^about$', about),
)
