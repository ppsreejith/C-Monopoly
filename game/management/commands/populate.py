from django.core.management.base import BaseCommand
from game.tests import createUser, createState, createEnergyIndustry,\
    createProductIndustry, createTransport, createCalamity
from govt.models import State
from game.models import GlobalConstants
from transport.models import Transport
from industry.models import ProductIndustry
from calamity.models import Calamity
from energy.models import EnergyIndustry
import random
from subprocess import call
from pipes import quote
from os.path import abspath

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        doRandom =  'random' in args
        doUsers = 'users' in args
        default = 'default' in args
        
        self.initVar()
        return self.populate(doRandom, doUsers, default)
    
    def populate(self, doRandom, doUsers, default):
        
        stateValues = self.stateValues
        productValues = self.productValues
        medProductValues = self.medProductValues
        bigProductValues = self.bigProductValues
        energyValues = self.energyValues
        medEnergyValues = self.medEnergyValues
        bigEnergyValues = self.bigEnergyValues
        calamityValues = self.calamityValues
        transportValues = self.transportValues
        coordinates = self.coordinates
        
        nameDef = "test2609_"
        profiles = []
        
        if doUsers:
            limit = 100
            print "Generating %d users"%limit
            for i in range(1,limit+1):
                profiles.append(createUser(i,
                                           extra_energy = 50, 
                                           energy_capacity = 300))
            print "%d Users generated"%limit
        
        states =[]
        stateIds = []
        others = []
        
        if default:
            if raw_input("All existing data will be removed from the database. Proceed? ([y]/n)") == "n":
                return
            comm = "python " + quote(abspath("manage.py")) + " flush"
            call( comm , shell = True)
            tempStates = State.objects.using('default_data').all()
            globalConstant = GlobalConstants.objects.using('default_data').all()
            tempProducts = ProductIndustry.objects.using('default_data').all()
            tempEnergies = EnergyIndustry.objects.using('default_data').all()
            tempTransports = Transport.objects.using('default_data').all()
            tempCalamities = Calamity.objects.using('default_data').all()
            
            for globConst in globalConstant:
                globConst.save(using='default')
            print "GlobalConstants created."
            for state in tempStates:
                state.save(using='default')
            print "States created."
            for product in tempProducts:
                product.save(using='default')
            print "ProductIndustries created."
            for energy in tempEnergies:
                energy.save(using='default')
            print "EnergyIndustries created."
            for transport in tempTransports:
                transport.save(using='default')
            print "Transports created."
            for calamity in tempCalamities:
                calamity.save(using='default')
            print "Calamities created."
        elif doRandom:
            stateLimit = 28
            print "Generating %d states"%stateLimit
            for i in range(0,stateLimit):
                obj = dict(stateValues)
                obj['name'] = nameDef+str(i)
                obj['population'] += random.randint(0,150) - 75
                obj['coordx'] = coordinates[i]["coordx"]
                obj['coordy'] = coordinates[i]["coordy"]
                states.append(createState(**obj))
                stateIds.append(states[i].id)
            print "%d States generated"%stateLimit
            spLimit = 10
            print "Generating %d small product industries"%spLimit
            for i in range(0,spLimit):
                obj = dict(productValues)
                vals =  random.sample( range(60),5 )
                obj['name'] = nameDef+"sf"+str(i)
                obj['maintenance_energy'] += vals[0]/10
                obj['energy_per_unit'] += vals[1]/100000.0
                obj['cost_price'] += vals[2]/10000.0
                obj['initial_cost'] += vals[3]/10.0
                obj['maintenance_cost'] += vals[4]/1000.0
                obj['states'] = random.sample(stateIds,random.randint(1,10))
                others.append(createProductIndustry(**obj))
            print "%d Small product industries generated"%spLimit
            mpLimit = 5
            print "Generating %d medium product industries"%mpLimit
            for i in range(0,mpLimit):
                obj = dict(medProductValues)
                obj['name'] = nameDef+"mf"+str(i)
                vals =  random.sample( range(60),5 )
                obj['maintenance_energy'] += vals[0]
                obj['energy_per_unit'] += vals[1]/10000.0
                obj['cost_price'] += vals[2]/1000.0
                obj['initial_cost'] += vals[3]
                obj['maintenance_cost'] += vals[4]/100.0
                obj['states'] = random.sample(stateIds,random.randint(1,10))
                others.append(createProductIndustry(**obj))
            print "%d Medium product industries generated"%mpLimit
            bpLimit = 2
            print "Generating %d big product industries"%bpLimit
            for i in range(0,bpLimit):
                obj = dict(bigProductValues)
                obj['name'] = nameDef+"bf"+str(i)
                vals =  random.sample( range(60),5 )
                obj['maintenance_energy'] += vals[0]*10
                obj['energy_per_unit'] += vals[1]/1000.0
                obj['cost_price'] += vals[2]/100.0
                obj['initial_cost'] += vals[3]*10.0
                obj['maintenance_cost'] += vals[4]/10.0
                obj['states'] = random.sample(stateIds,random.randint(1,10))
                others.append(createProductIndustry(**obj))
            print "%d Big product industries generated"%bpLimit
            seLimit = 6
            print "Generating %d small energy industries"%seLimit
            for i in range(0,seLimit):
                obj = dict(energyValues)
                obj['name'] = nameDef+"sp"+str(i)
                vals =  random.sample( range(60),3 )
                obj['initial_cost'] += vals[0]/10.0
                obj['maintenance_cost'] += vals[1]/1000.0
                obj['carbon_per_unit'] += vals[2]/100.0
                obj['states'] = random.sample(stateIds,random.randint(1,10))
                others.append(createEnergyIndustry(**obj))
            print "%d Small energy industries generated"%seLimit
            meLimit = 3
            print "Generating %d medium energy industries"%meLimit
            for i in range(0,meLimit):
                obj = dict(medEnergyValues)
                obj['name'] = nameDef+"mp"+str(i)
                vals =  random.sample( range(60),3 )
                obj['initial_cost'] += vals[0]/1.0
                obj['maintenance_cost'] += vals[1]/100.0
                obj['carbon_per_unit'] += vals[2]/10.0
                obj['states'] = random.sample(stateIds,random.randint(1,10))
                others.append(createEnergyIndustry(**obj))
            print "%d Medium energy industries generated"%meLimit
            beLimit = 1
            print "Generating %d big energy industry"%beLimit
            for i in range(0,beLimit):
                obj = dict(bigEnergyValues)
                obj['name'] = nameDef+"bp"+str(i)
                vals =  random.sample( range(60),3 )
                obj['initial_cost'] += vals[0]*10.0
                obj['maintenance_cost'] += vals[1]/10.0
                obj['carbon_per_unit'] += vals[2]/1.0
                obj['states'] = random.sample(stateIds,random.randint(1,10))
                others.append(createEnergyIndustry(**obj))
            print "%d Big energy industry generated"%beLimit
            tLimit = 3
            print "Generating %d transports"%tLimit
            for i in range(0,tLimit):
                obj = dict(transportValues)
                obj['name'] = nameDef+str(i)
                vals =  random.sample( range(1,60),3 )
                obj['initial_cost'] += vals[0]
                obj['stopping_cost'] += vals[1]/100.0
                obj['travel_rate'] += vals[2]/1000.0
                obj['states'] = random.sample(stateIds,random.randint(4,8))
                others.append(createTransport(**obj))
            print "%d Transports generated"%tLimit
            cLimit = 5
            print "Generating %d calamities"%cLimit
            for i in range(0,cLimit):
                obj = dict(calamityValues)
                obj['name'] = nameDef+str(i)
                vals =  random.sample( range(1,10),3 )
                obj['severity'] += vals[0]*5-20
                obj['probability_number'] = vals[1]
                obj['states'] = random.sample(stateIds,random.randint(4,10))
                others.append(createCalamity(**obj))
            print "%d Calamities generated"%cLimit
        
        if not any([doRandom, doUsers, default]):
            print """
The available commands are random, users, default.
They are used to generate users, states, transports, industries and calamities
They are described as follows:
random \t Generates random values for all,
users \t Generates 100 random users,
default \t Retrieves default set values for all,
"""
    
    def initVar(self):
        self.stateValues = {
             'population' : 90,
             'coordx':90,
             'coordy':23,
             }
        self.productValues = {
            'maintenance_energy' : 2,
            'energy_per_unit' : 0.0003,
            'cost_price' : 0.004,
            'initial_cost' : 12,
            'maintenance_cost':0.5,
            'carbon_per_unit' : 0.003,
            }
        self.medProductValues = {
            'maintenance_energy' : 11,
            'energy_per_unit' : 0.003,
            'cost_price' : 0.03,
            'initial_cost' : 105,
            'maintenance_cost':3,
            'carbon_per_unit' : 0.03,
            }
        self.bigProductValues = {
            'maintenance_energy' : 94,
            'energy_per_unit' : 0.03,
            'cost_price' : 0.2,
            'initial_cost' : 1200,
            'maintenance_cost':10,
            'carbon_per_unit' : 0.3,
            }
        self.energyValues = {
            'initial_cost' : 20,
            'maintenance_cost' : 0.03,
            'carbon_per_unit' : 0.3,
            'output' : 1,
            }
        self.medEnergyValues = {
            'initial_cost' : 200,
            'maintenance_cost' : 0.3,
            'carbon_per_unit' : 3,
            'output' : 14,
            }
        self.bigEnergyValues = {
            'initial_cost' : 2000,
            'maintenance_cost' : 3,
            'carbon_per_unit' : 30,
            'output' : 200,
            }
        self.calamityValues = {
            'severity' : 40,
            'probability_number' : 5,
            }
        self.transportValues = {
            'initial_cost' : 80,
            'stopping_cost' : 0.3,
            'travel_rate' : 0.03,
            'carbon_cost_rate' : 0.05,
            'energy_rate' : 0.3,
            }
        self.coordinates = [{"coordx":72,"coordy":22},{"coordx":73,"coordy":23},{"coordx":74,"coordy":15},{"coordx":77,"coordy":13},{"coordx":77,"coordy":30},{"coordx":73,"coordy":19},{"coordx":74,"coordy":26},{"coordx":78,"coordy":30},{"coordx":80,"coordy":27},{"coordx":77,"coordy":8},{"coordx":85,"coordy":25},{"coordx":76,"coordy":31},{"coordx":81,"coordy":21},{"coordx":77,"coordy":31},{"coordx":85,"coordy":20},{"coordx":91,"coordy":24},{"coordx":94,"coordy":25},{"coordx":93,"coordy":27},{"coordx":92,"coordy":25},{"coordx":92,"coordy":23},{"coordx":78,"coordy":17},{"coordx":88,"coordy":22},{"coordx":88,"coordy":27},{"coordx":80,"coordy":13},{"coordx":85,"coordy":23},{"coordx":77,"coordy":29},{"coordx":76,"coordy":33},{"coordx":91,"coordy":26}];
