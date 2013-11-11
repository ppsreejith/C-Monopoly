from django.core.management.base import BaseCommand
from govt.models import State
from django.contrib.auth.models import User
from industry.models import Factory, ProductIndustry
from energy.models import EnergyIndustry
from transport.models import Transport
from calamity.models import Calamity

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        nameDef = "test2609_"
        every =  'all' in args
        if every or 'users' in args:
            User.objects.filter(username__startswith = nameDef ).delete()
        if every or 'states' in args:
            State.objects.filter(name__startswith = nameDef ).delete()
            ProductIndustry.objects.filter(name__startswith = nameDef ).delete()
            ProductIndustry.objects.filter(name__startswith = nameDef ).delete()
            ProductIndustry.objects.filter(name__startswith = nameDef ).delete()
            EnergyIndustry.objects.filter(name__startswith = nameDef ).delete()
            EnergyIndustry.objects.filter(name__startswith = nameDef ).delete()
            EnergyIndustry.objects.filter(name__startswith = nameDef ).delete()
            Transport.objects.filter(name__startswith = nameDef).delete()
            Calamity.objects.filter(name__startswith = nameDef).delete()