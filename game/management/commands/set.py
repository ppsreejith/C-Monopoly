from django.core.management.base import BaseCommand
from subprocess import call
from govt.models import State
from game.models import GlobalConstants
from transport.models import Transport
from industry.models import ProductIndustry
from calamity.models import Calamity
from energy.models import EnergyIndustry
from os.path import join,dirname,abspath
from pipes import quote
import random

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        print("Note that before setting default data, you must clear the default data.\n")
        if raw_input("Are you sure you want to proceed to set current data as default data? ([y]/n)\n") in ("n","N"):
            return
        
        words = ["geremih","amrav","rishicomplex","d226nhr"]
        rword = words[random.randint(0,len(words)-1)]
        
        if raw_input("Please enter the following word in uppercase: %s \n"%rword) != rword.upper():
            return
        
        rm_old = "rm " + quote(join(abspath('cmonopoly'), "default_data.sqlite3"))
        sync_new = "python " + quote(abspath('manage.py')) + " syncdb --database=default_data"
        migrate_new = "python " + quote(abspath("manage.py")) + " migrate --database=default_data > /dev/null"
        
        call( rm_old ,shell=True)
        call( sync_new ,shell=True)
        print "Please Wait.."
        call( migrate_new ,shell=True)
        print "Done Creating, now copying data.."
        
        #GlobalConstants, States, Transports, ProductIndustries, 
        #EnergyIndustries, Calamities
        globalConstant = GlobalConstants.objects.all()
        for it in globalConstant:
            it.save(using = 'default_data')
        states = State.objects.all()
        for it in states:
            it.save(using = 'default_data')
        trans = Transport.objects.all()
        for it in trans:
            it.save(using = 'default_data')
        prods = ProductIndustry.objects.all()
        for it in prods:
            it.save(using = 'default_data')
        energs = EnergyIndustry.objects.all()
        for it in energs:
            it.save(using = 'default_data')
        calamities = Calamity.objects.all()
        for it in calamities:
            it.save(using = 'default_data')
        print "Done. Data successefully set to default."
