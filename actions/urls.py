from django.conf.urls import patterns, url
from actions.views import User, Factories, Powerplants, Transports, Loans


urlpatterns = patterns('',
     url(r'^user$',User.as_view()),
     url(r'^factories$',Factories.as_view()),
     url(r'^powerplants',Powerplants.as_view()),
     url(r'^transports',Transports.as_view()),
     url(r'^loans',Loans.as_view()),
)