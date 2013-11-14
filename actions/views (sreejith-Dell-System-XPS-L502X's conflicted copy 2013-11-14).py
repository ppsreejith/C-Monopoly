from game.views import ApiTemplate
from actions.models import Profile
from industry.models import Factory, LoansCreated
from energy.models import PowerPlant
from transport.models import TransportCreated
from collections import defaultdict

class User(ApiTemplate):
    def get(self,request):
        return self.render(Profile.objects.values('user__username','capital','netWorth','rank','extra_energy','energy_capacity').get(user__id = request.session.get('user_id')))

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
        loans = list(LoansCreated.objects.filter(player__user__id = request.session.get('user_id')).values())
        return self.render(loans)