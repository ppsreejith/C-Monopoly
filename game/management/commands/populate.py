from django.core.management.base import BaseCommand
from game.tests import createUser, createState, createEnergyIndustry,\
    createProductIndustry, createTransport, createCalamity
import random

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        nameDef = "test2609_"
        every =  'random' in args
        everyReal = 'real' in args
        
        stateValues = {
             'population' : 90,
             'coordx':90,
             'coordy':23,
             }
        productValues = {
            'maintenance_energy' : 2,
            'energy_per_unit' : 0.0003,
            'cost_price' : 0.004,
            'initial_cost' : 12,
            'maintenance_cost':0.5,
            'carbon_per_unit' : 0.003,
            }
        medProductValues = {
            'maintenance_energy' : 11,
            'energy_per_unit' : 0.003,
            'cost_price' : 0.03,
            'initial_cost' : 105,
            'maintenance_cost':3,
            'carbon_per_unit' : 0.03,
            }
        bigProductValues = {
            'maintenance_energy' : 94,
            'energy_per_unit' : 0.03,
            'cost_price' : 0.2,
            'initial_cost' : 1200,
            'maintenance_cost':10,
            'carbon_per_unit' : 0.3,
            }
        energyValues = {
            'initial_cost' : 20,
            'maintenance_cost' : 0.03,
            'carbon_per_unit' : 0.3,
            'output' : 1,
            }
        medEnergyValues = {
            'initial_cost' : 200,
            'maintenance_cost' : 0.3,
            'carbon_per_unit' : 3,
            'output' : 14,
            }
        bigEnergyValues = {
            'initial_cost' : 2000,
            'maintenance_cost' : 3,
            'carbon_per_unit' : 30,
            'output' : 200,
            }
        calamityValues = {
            'severity' : 40,
            'probability_number' : 5,
            }
        transportValues = {
            'initial_cost' : 80,
            'stopping_cost' : 0.3,
            'travel_rate' : 0.03,
            'carbon_cost_rate' : 0.05,
            'energy_rate' : 0.3,
            }
        coordinates = [{"coordx":72,"coordy":22},{"coordx":73,"coordy":23},{"coordx":74,"coordy":15},{"coordx":77,"coordy":13},{"coordx":77,"coordy":30},{"coordx":73,"coordy":19},{"coordx":74,"coordy":26},{"coordx":78,"coordy":30},{"coordx":80,"coordy":27},{"coordx":77,"coordy":8},{"coordx":85,"coordy":25},{"coordx":76,"coordy":31},{"coordx":81,"coordy":21},{"coordx":77,"coordy":31},{"coordx":85,"coordy":20},{"coordx":91,"coordy":24},{"coordx":94,"coordy":25},{"coordx":93,"coordy":27},{"coordx":92,"coordy":25},{"coordx":92,"coordy":23},{"coordx":78,"coordy":17},{"coordx":88,"coordy":22},{"coordx":88,"coordy":27},{"coordx":80,"coordy":13},{"coordx":85,"coordy":23},{"coordx":77,"coordy":29},{"coordx":76,"coordy":33},{"coordx":91,"coordy":26}];
        
        profiles = []
        realStates = self.getRealStates()
        if every or 'users' in args:
            limit = 100
            print "Generating %d users"%limit
            for i in range(1,limit+1):
                profiles.append(createUser(i,
                                           extra_energy = 50, 
                                           energy_capacity = 300))
            print "%d Users generated"%limit
        
        states =[]
        stateIds = []
        sfactories = []
        mfactories = []
        bfactories = []
        spowerplants = []
        mpowerplants = []
        bpowerplants = []
        transports = []
        calamities = []
        
        if everyReal:
            tempStates = self.getRealStates()
            for i,state in enumerate(tempStates):
                states.append(createState(**state))
                stateIds.append(states[i].id)
        
        #couting on probability
        if every or 'states' in args:
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
                sfactories.append(createProductIndustry(**obj))
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
                mfactories.append(createProductIndustry(**obj))
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
                bfactories.append(createProductIndustry(**obj))
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
                spowerplants.append(createEnergyIndustry(**obj))
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
                mpowerplants.append(createEnergyIndustry(**obj))
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
                bpowerplants.append(createEnergyIndustry(**obj))
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
                transports.append(createTransport(**obj))
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
                calamities.append(createCalamity(**obj))
            print "%d Calamities generated"%cLimit
    def getRealStates(self):
        return [{'name':'Uttar Pradesh',
                 'population':100,
                 'growth_rate':2.02,
                 'coordx':80,
                 'coordy':27,
                 'income':12.5,
                 'income_growth_rate':5.6,
                 },
                 {'name':'Maharashtra',
                 'population':66,
                 'growth_rate':1.6,
                 'coordx':73,
                 'coordy':19,
                 'income':25,
                 'income_growth_rate':9.3,
                 },
                 {'name':'Bihar',
                 'population':52,
                 'growth_rate':2.5,
                 'coordx':85,
                 'coordy':25,
                 'income':10,
                 'income_growth_rate':10,
                 },
                 {'name':'West Bengal',
                 'population':45,
                 'growth_rate':1.3,
                 'coordx':88,
                 'coordy':22,
                 'income':20,
                 'income_growth_rate':8,
                 }]