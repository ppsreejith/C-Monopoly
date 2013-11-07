from django.core.management.base import BaseCommand
from game.tests import createUser, createState, createEnergyIndustry,\
    createProductIndustry, createTransport, createCalamity
import random

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        stateValues = {
             'population' : 90,
             'coordx':90,
             'coordy':23,
             }
        productValues = {
            'maintenance_energy' : 0.002,
            'energy_per_unit' : 0.0003,
            'cost_price' : 0.004,
            'initial_cost' : 12,
            'maintenance_cost':0.01,
            'carbon_per_unit' : 0.003,
            }
        medProductValues = {
            'maintenance_energy' : 0.02,
            'energy_per_unit' : 0.003,
            'cost_price' : 0.03,
            'initial_cost' : 105,
            'maintenance_cost':0.1,
            'carbon_per_unit' : 0.03,
            }
        bigProductValues = {
            'maintenance_energy' : 0.2,
            'energy_per_unit' : 0.03,
            'cost_price' : 0.2,
            'initial_cost' : 1200,
            'maintenance_cost':1,
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
        
        nameDef = "test2609_"
        every =  'all' in args
        
        profiles = []
        if every or 'users' in args:
            for i in range(1,100):
                profiles.append(createUser(i,
                                           extra_energy = 50, 
                                           energy_capacity = 300))
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
        if every or 'states' in args:
            for i in range(0,20):
                obj = dict(stateValues)
                obj['name'] = nameDef+str(i)
                obj['population'] += random.randint(0,150) - 75
                obj['coordx'] += random.randint(0,60) - 30
                obj['coordy'] += random.randint(0,30) - 15
                states.append(createState(**obj))
                stateIds.append(states[i].id)
            for i in range(0,10):
                obj = dict(productValues)
                vals =  random.sample( range(60),5 )
                obj['name'] = nameDef+"sf"+str(i)
                obj['maintenance_energy'] += vals[0]/10000.0
                obj['energy_per_unit'] += vals[1]/100000.0
                obj['cost_price'] += vals[2]/10000.0
                obj['initial_cost'] += vals[3]/10.0
                obj['maintenance_cost'] += vals[4]/1000.0
                obj['states'] = random.sample(stateIds,random.randint(1,10))
                sfactories.append(createProductIndustry(**obj))
            for i in range(0,5):
                obj = dict(medProductValues)
                obj['name'] = nameDef+"mf"+str(i)
                vals =  random.sample( range(60),5 )
                obj['maintenance_energy'] += vals[0]/1000.0
                obj['energy_per_unit'] += vals[1]/10000.0
                obj['cost_price'] += vals[2]/1000.0
                obj['initial_cost'] += vals[3]
                obj['maintenance_cost'] += vals[4]/100.0
                obj['states'] = random.sample(stateIds,random.randint(1,10))
                mfactories.append(createProductIndustry(**obj))
            for i in range(0,2):
                obj = dict(bigProductValues)
                obj['name'] = nameDef+"bf"+str(i)
                vals =  random.sample( range(60),5 )
                obj['maintenance_energy'] += vals[0]/100.0
                obj['energy_per_unit'] += vals[1]/1000.0
                obj['cost_price'] += vals[2]/100.0
                obj['initial_cost'] += vals[3]*10.0
                obj['maintenance_cost'] += vals[4]/10.0
                obj['states'] = random.sample(stateIds,random.randint(1,10))
                bfactories.append(createProductIndustry(**obj))
            for i in range(0,6):
                obj = dict(energyValues)
                obj['name'] = nameDef+"sp"+str(i)
                vals =  random.sample( range(60),3 )
                obj['initial_cost'] += vals[0]/10.0
                obj['maintenance_cost'] += vals[1]/1000.0
                obj['carbon_per_unit'] += vals[2]/100.0
                obj['states'] = random.sample(stateIds,random.randint(1,10))
                spowerplants.append(createEnergyIndustry(**obj))
            for i in range(0,3):
                obj = dict(energyValues)
                obj['name'] = nameDef+"mp"+str(i)
                vals =  random.sample( range(60),3 )
                obj['initial_cost'] += vals[0]/1.0
                obj['maintenance_cost'] += vals[1]/100.0
                obj['carbon_per_unit'] += vals[2]/10.0
                obj['states'] = random.sample(stateIds,random.randint(1,10))
                mpowerplants.append(createEnergyIndustry(**obj))
            for i in range(0,1):
                obj = dict(energyValues)
                obj['name'] = nameDef+"bp"+str(i)
                vals =  random.sample( range(60),3 )
                obj['initial_cost'] += vals[0]*10.0
                obj['maintenance_cost'] += vals[1]/10.0
                obj['carbon_per_unit'] += vals[2]/1.0
                obj['states'] = random.sample(stateIds,random.randint(1,10))
                bpowerplants.append(createEnergyIndustry(**obj))
            for i in range(0,3):
                obj = dict(transportValues)
                obj['name'] = nameDef+str(i)
                vals =  random.sample( range(1,60),3 )
                obj['initial_cost'] += vals[0]
                obj['stopping_cost'] += vals[1]/100.0
                obj['travel_rate'] += vals[2]/1000.0
                obj['states'] = random.sample(stateIds,random.randint(4,8))
                transports.append(createTransport(**obj))
            for i in range(0,5):
                obj = dict(calamityValues)
                obj['name'] = nameDef+str(i)
                vals =  random.sample( range(1,10),3 )
                obj['severity'] += vals[0]*5-20
                obj['probability_number'] = vals[1]
                obj['states'] = random.sample(stateIds,random.randint(4,10))
                calamities.append(createCalamity(**obj))