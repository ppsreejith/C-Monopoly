from django.conf.urls import patterns, url
from actions.views import User, Factories, Powerplants, Transports, Loans,\
    EnergyMarket, Dates, Logs


urlpatterns = patterns('',
     url(r'^user$',User.as_view()),
     url(r'^factories$',Factories.as_view()),
     url(r'^powerplants',Powerplants.as_view()),
     url(r'^transports',Transports.as_view()),
     url(r'^loans',Loans.as_view()),
     url(r'^energymarket',EnergyMarket.as_view()),
     url(r'^date',Dates.as_view()),
     url(r'^logbook',Logs.as_view()),
)