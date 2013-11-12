from game.views import ApiTemplate
from actions.models import Profile
from industry.models import Factory
from energy.models import PowerPlant
from transport.models import TransportCreated
from collections import defaultdict

class User(ApiTemplate):
    def get(self,request):
        return self.render(Profile.objects.values('capital','netWorth','rank','extra_energy','energy_capacity').get(user = request.user))

class Factories(ApiTemplate):
    def get(self,request):
        profile = Profile.objects.get(user = request.user)
        factories = Factory.objects.filter(player = profile).values()
        return self.render(list(factories))

class Powerplants(ApiTemplate):
    def get(self,request):
        profile = Profile.objects.get(user = request.user)
        plants = PowerPlant.objects.filter(player = profile).values()
        return self.render(list(plants))

class Transports(ApiTemplate):
    def get(self,request):
        profile = Profile.objects.get(user = request.user)
        transportList = list(TransportCreated.objects.filter(player = profile).values())
        transportStates = TransportCreated.states.through.objects.values('transportcreated__id','state__id')  # @UndefinedVariable
        tList = defaultdict(lambda:[])
        for tr in transportStates:
            tList[tr['transportcreated__id']].append(tr['state__id'])
        for transport in transportList:
            transport['states'] = tList[transport['id']]
        return self.render(transportList)