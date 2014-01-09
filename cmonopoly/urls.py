from django.conf.urls import patterns, include, url
from game.views import index, leave
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
     url(r'^admin/', include(admin.site.urls)),
     url(r'^$',index),
     url(r'^login$',TemplateView.as_view(template_name = "login.html"), name = "login"),
     url(r'^logout$', leave, name = "logout"),
     url(r'^api/',include('actions.urls'))
)