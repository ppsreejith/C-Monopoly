from django.core.management.base import BaseCommand
from govt.models import State
from django.contrib.auth.models import User
from industry.models import Factory, ProductIndustry
from energy.models import EnergyIndustry
from transport.models import Transport
from calamity.models import Calamity

class Command(BaseCommand):
    """
    Used for removing automatically generated data from database.
    """
    
    def handle(self, *args, **options):
        every =  'all' in args
        doUsers = 'users' in args
        doStates = 'states' in args
        
        nameDef = "test2609_"
        
        if every or doUsers:
            User.objects.filter(username__startswith = nameDef ).delete()
            self.stdout.write( "Removed Users." )
        if every or doStates:
            State.objects.filter(name__startswith = nameDef ).delete()
            ProductIndustry.objects.filter(name__startswith = nameDef ).delete()
            EnergyIndustry.objects.filter(name__startswith = nameDef ).delete()
            Transport.objects.filter(name__startswith = nameDef).delete()
            Calamity.objects.filter(name__startswith = nameDef).delete()
            self.stdout.write( "Removed states, industries, transports and calamities" )
        if not any([every, doUsers, doStates]):
            self.stdout.write("""
The available commands are all, users, states.
They are used to remove users, states, transports, industries and calamities starting with {0}
They are described as follows:

all \t Removes everything
users \t Removes users starting with {0}
states \t Removes states, transports, industries and calamities starting with {0}
            """.format(nameDef) )
