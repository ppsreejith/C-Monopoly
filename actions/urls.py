from django.conf.urls import patterns, url
from actions.views import SimpleTest


urlpatterns = patterns('',
     url(r'^test$',SimpleTest.as_view())
)