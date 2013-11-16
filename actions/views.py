from game.views import ApiTemplate
from actions.models import Profile
from industry.models import Factory, LoansCreated
from energy.models import PowerPlant
from transport.models import TransportCreated
from collections import defaultdict
from django.db import connection
import random
from game.models import GlobalConstants
from player.models import LogBook

class User(ApiTemplate):
    def get(self,request):
        return self.render(Profile.objects.values('user__username','capital','netWorth','rank','extra_energy','energy_capacity','selling_energy').get(user__id = request.session.get('user_id')))

class Factories(ApiTemplate):
    def get(self,request):
        factories = list(Factory.objects.filter(player__user__id = request.session.get('user_id')).values())
        return self.render(factories)

class Powerplants(ApiTemplate):
    def get(self,request):
        plants = list(PowerPlant.objects.filter(player__user__id = request.session.get('user_id')).values())
        return self.render(plants)

class Transports(ApiTemplate):
    def get(self,request):
        transportList = list(TransportCreated.objects.filter(player__user__id = request.session.get('user_id')).values())
        transportStates = TransportCreated.states.through.objects.values('transportcreated__id','state__id')  # @UndefinedVariable
        tList = defaultdict(lambda:[])
        for tr in transportStates:
            tList[tr['transportcreated__id']].append(tr['state__id'])
        for transport in transportList:
            transport['states'] = tList[transport['id']]
        return self.render(transportList)

class Loans(ApiTemplate):
    def get(self, request):
        loanList = list(LoansCreated.objects.filter(player__user__id = request.session.get('user_id')).values())
        factories = LoansCreated.mortaged_industries.through.objects.values('loanscreated__id', 'factory__id')  # @UndefinedVariable
        lList = defaultdict(lambda:[])
        for factory in factories:
            lList[factory['loanscreated__id']].append(factory['factory__id'])
        for loan in loanList:
            loan['factories'] = lList[loan['id']] 
        return self.render(loanList)

class EnergyMarket(ApiTemplate):
    def get(self, request):
        rand = random.randint(1,Profile.objects.count() - 20)
        limit = 9
        users = list(Profile.objects.filter(selling_energy = False).filter(rank__gte = rand).values('id','user__username','rank','extra_energy')[:limit])
        return self.render(users)

class Dates(ApiTemplate):
    def get(self, request):
        curDate = GlobalConstants.objects.values('current_day','current_month','current_year').get();
        return self.render(curDate)

class Logs(ApiTemplate):
    def get(self, request):
        logs = list(LogBook.objects.filter(player__user__id = request.session['user_id']).order_by('id').values('message','id'))
        return self.render(logs)

class Ranks(ApiTemplate):
    def get(self, request):
        players = list(Profile.objects.order_by('rank').values('id','rank','user__username','capital','netWorth')[:10])
        return self.render(players)