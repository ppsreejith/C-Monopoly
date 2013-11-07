from django.conf.urls import patterns, include, url
from game.views import index
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
     url(r'^admin/', include(admin.site.urls)),
     url(r'^$',index),
     url(r'^api/',include('actions.urls'))
)