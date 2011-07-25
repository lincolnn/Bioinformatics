from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^polls/$', 'polls.views.index'),

    (r'^polls/(?P<poll_id>\d+)/$', 'polls.views.detail'),

    (r'^polls/(?P<poll_id>\d+)/results/$',    
      'polls.views.results'),

    (r'^polls/(?P<poll_id>\d+)/vote/$',
      'polls.views.vote'),

    url(r'^admin/', include(admin.site.urls)),
)    
