from django.test import TestCase
from game.models import GlobalConstants
from django.contrib.auth.models import User
from django.db import IntegrityError
from actions.models import Profile
from industry.models import ProductIndustry, Factory
from govt.models import State
from energy.models import EnergyIndustry
from calamity.models import Calamity
from transport.models import Transport, TransportCreated
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import connection

"""
Created by ppsreejith.
Module which contains functions for generating game constants and Unit tests.
"""

def createUser(no, extra_energy = 5, energy_capacity =30):
    """Creates a user and profile class according to supplied arguments.
    
    Args:
        no - A number to uniqely identify constant.
        extra_energy - Extra energy of user to assign. Default value 5
        energy_capacity - Energy Capacity of player. Default value 30
    """
    
    user = User.objects.create_user("test2609_%d"%no, "test2609_%d@gmail.com"%no, "password")
    profile = Profile(user = user, extra_energy = extra_energy, energy_capacity = energy_capacity)
    profile.save()
    return profile

def startMeasure():
    """
    Used for debugging and finding out number of database calls.
    endMeasure must be called afterwards to end it. connection.queries
    can be used to log the database calls made.
    """
    
    settings.DEBUG = True
    connection.queries = []
    return connection.queries

def endMeasure():
    """ Called to end logging database calls. """
    settings.DEBUG = False

def createProductIndustry(name = "Coconut",maintenance_energy = 4,energy_per_unit = 0.5,
                          unit = "Pieces",research_level = 1,annual_value_decrease = 5.4,cost_price = 1,
                          maintenance_cost = 1,initial_cost = 5,carbon_per_unit = 0.003,states = [1,2,3,4]):
    """
    Creates a Product Industry given the details.
    
    Args:
      Arguments are the various fields of the ProductIndustry model.
    """
    industry = ProductIndustry(name = name,maintenance_energy = maintenance_energy,cost_price = cost_price,
                               energy_per_unit = energy_per_unit,unit = unit,research_level = research_level,
                               annual_value_decrease = annual_value_decrease,maintenance_cost = maintenance_cost,
                               initial_cost = initial_cost,carbon_per_unit = carbon_per_unit)
    industry.save()
    industry.states.add(*states)
    industry.save()
    return industry

def createEnergyIndustry(name = "Coal",research_level = 1,output = 5,
                         annual_value_decrease = 5.4,maintenance_cost = 1,initial_cost = 5,
                         carbon_per_unit = 0.003,states = [1,2,3,4]):
    """
    Creates an Energy Industry given the details.
    
    Args:
      Arguments are the various fields of the EnergyIndustry model.
    """
    
    industry = EnergyIndustry(name = name,research_level = research_level,output = output,
                               annual_value_decrease = annual_value_decrease,maintenance_cost = maintenance_cost,
                               initial_cost = initial_cost,carbon_per_unit = carbon_per_unit)
    industry.save()
    industry.states.add(*states)
    industry.save()
    return industry
    
def createCalamity(name = "Tornado",severity = 80, probability_number = 0.02, states = [2,3,4,5]):
    """
    Creates a Calamity given the details.
    
    Args:
      Arguments are the various fields of the Calamity model.
    """
    
    calamity = Calamity(name = name, probability_number = probability_number, severity = severity)
    calamity.save()
    calamity.states.add(*states)
    calamity.save()
    return calamity

def createState(name = "Telengana",coordx = 6, coordy = 4,population = 34.5,
                research_level = 1, capacity = 30, energy_plant_capacity = 20, income = 30.4, 
                growth_rate = 4.5, income_growth_rate = 4.5):
    """
    Creates a State given the details.
    
    Args:
      Arguments are the various fields of the State model.
    """
    
    state = State(name = name, coordx = coordx, coordy = coordy, population = population,
                        research_level = research_level, capacity = capacity,growth_rate = growth_rate,
                        energy_plant_capacity = energy_plant_capacity, income = income,
                        income_growth_rate = income_growth_rate)
    state.save()
    return state

def createTransport(name = "Train",research_level = 1,energy_rate=0.2,
                    max_stops = 6,stopping_cost = 40,travel_rate = 30,
                    initial_cost = 5,carbon_cost_rate = 0.003,states = [1,2,3,4]):
    """
    Creates a Transport given the details.
    
    Args:
      Arguments are the various fields of the Transport model.
    """
    
    transport = Transport(name = name, research_level = research_level, energy_rate = energy_rate,
                          max_stops = max_stops, stopping_cost = stopping_cost, travel_rate = travel_rate,
                          initial_cost = initial_cost, carbon_cost_rate = carbon_cost_rate)
    transport.save()
    transport.states.add(*states)
    transport.save()
    return transport

class ModelsTestCase(TestCase):
    """
    Class for Unit testing.
    """
    
    def setUp(self):
        """Initialize unit testing"""
        
        #Set up global constants
        globalConstants = GlobalConstants(carbon_buying_price = 100,
                                          energy_buying_price = 80,
                                          energy_selling_price = 100,
                                          tax_rate = 10,
                                          loan_interest_rate = 20,
                                          vehicle_variable_limit = 10,
                                          max_research_level = 4,
                                          initial_research_time = 8,
                                          monthly_research_cost = 80,
                                          initial_capital = 100,)
        globalConstants.full_clean()
        globalConstants.save()
        
        #Create a default player
        self.profile = createUser(1)
        s1 = self.state1 = createState()
        s2 = self.state2 = createState(name = "Bihar",coordx = 10, coordy = 20)
        s3 = self.state3 = createState(name = "Rajasthan",coordx = 10, coordy = 30)
        s4 = self.state4 = createState(name = "Andhra Pradesh",coordx = 15, coordy = 20)
        s5 = self.state5 = createState(name = "Kashmir",coordx = 10, coordy = 11)
        s6 = self.state6 = createState(name = "Assam",coordx = 25, coordy = 11, research_level=2)
        self.prodInd1 = createProductIndustry(states = [s1,s2,s3,s4,s6])
        self.prodInd2 = createProductIndustry(name = "Rubber",states = [s1,s2,s4,s5,s6])
        self.prodInd3 = createProductIndustry(name = "Coffee",states = [s1,s2,s4,s5,s6], research_level=2)
        self.energyInd1 = createEnergyIndustry(states = [s1,s2,s3,s4,s6])
        self.energyInd2 = createEnergyIndustry(name = "Biofuel",states = [s1,s2,s3,s4,s5,s6])
        self.energyInd3 = createEnergyIndustry(name = "Hydro",states = [s2,s3,s4,s5,s6], research_level=2)
        self.transport1 = createTransport(states = [s1,s3,s4,s5,s6])
        self.transport2 = createTransport(name = "Ship",states = [s1,s2,s3,s4,s5,s6], max_stops = 4)
        self.transport3 = createTransport(name = "Road",states = [s1,s2,s3,s4,s5,s6], research_level=2)
        self.calamity1 = createCalamity(states = [s2,s3,s4,s5,s6])
        self.calamity2 = createCalamity(name = "Hurricane",states = [s1,s2,s3,s5,s6])
        self.calamity3 = createCalamity(name = "Tsunami",states = [s1,s2,s3,s5,s6])
    
    def test_player(self):
        """ Method for testing players. """
        self.assertEqual(self.profile.capital, GlobalConstants.objects.get().initial_capital, "Default capital is wrong")
        self.assertEqual(self.profile.netWorth, GlobalConstants.objects.get().initial_capital, "Default net worth is wrong")
        
        #Test if two seperate players can be made with same values
        try:
            profile2 = createUser(2)
            profile3 = createUser(2)
            self.assert_(False, "Two players were created with same user")
        except IntegrityError:
            pass
    
    def test_loan_scenario(self):
        """ Method for testing Loans. """
        
        profile2 = createUser(3)
        
        #Testing whether factories can be built in the states where the Industry is not available.
        profile2.buy_factory(self.prodInd1.id,self.state1.id)
        profile2.buy_factory(self.prodInd1.id,self.state2.id)
        try:
            profile2.buy_factory(self.prodInd2.id,self.state3.id) #Should throw error. Factory not available in state3.
        except ValidationError:
            pass
        profile2.buy_factory(self.prodInd2.id,self.state4.id)
        self.assertEqual(profile2.factory_set.count(),3,"profile2 must possess only 3 factories")
        
        
        #Testing for loans.
        values = profile2.factory_set.values_list('id', flat=True)
        values = [int(i) for i in values]
        profile2 = Profile.objects.get(id = profile2.id)
        self.profile = Profile.objects.get(id = self.profile.id)
        capital_before_loan = profile2.capital
        netWorth_before_loan = profile2.netWorth
        try:
            profile2.takeLoan(100,values) #Too much amount for what is being mortaged.
        except Exception:
            pass
        profile2.takeLoan(5,values[0:2])
        try:
            self.profile.takeLoan(3,values[2]) #Can't take loan because he doesn't own that factory.
        except Exception:
            pass
        profile2 = Profile.objects.get(id = profile2.id)
        self.profile = Profile.objects.get(id = self.profile.id)
        self.assertTrue(hasattr(profile2,"Loan"),"Loan should've been successful")
        self.assertFalse(hasattr(self.profile,"Loan"), "Loan should've failed")  
        self.assertEqual(profile2.Loan.mortaged_industries.count(),2,"profile2 must mortage only 2 factories")
        self.assertEqual(float(profile2.Loan.amount)*float(profile2.Loan.time_remaining), 
                         5*(100.0 + float(GlobalConstants.objects.get().loan_interest_rate))/100, 
                         "Loan amount is incorrect") #profile2's loan must be Amount + interest
        self.assertEqual(float(profile2.capital), float(capital_before_loan) + 5.0,
                         "Capital is incorrect") #profile2's capital must be original + Loan Amount
        self.assertEqual(float(profile2.netWorth), 
                         float(netWorth_before_loan)-5.0*(float(GlobalConstants.objects.get().loan_interest_rate))/100.0, 
                         "Net worth is incorrect") #profile2's Net worth must be Networth - Amount lost due to taking a loan.
        print "Loans successfully tested"
    
    def test_energyDeal(self):
        """ Method for testing energy deals. """
        
        profile2 = createUser(4)
        profile3 = createUser(5)
        
        
        #Testing energy deal validation.
        try:
            profile2.proposeEnergyOffer(profile3.id, 3, 0.5) #Will fail to validate since other person's not ready to sell energy.
        except ValidationError:
            pass
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        profile3 = Profile.objects.get(id = profile3.id)
        self.assertFalse(hasattr(profile2,'EnergyContract') , "The energy offer should not've been proposed since it wasn't valid.")
        
        
        #Testing energy offer rejection.
        profile3.setSellingEnergy(True) #Now he is available for selling energy.
        profile2.proposeEnergyOffer(profile3.id, 3, 0.5)
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        profile3 = Profile.objects.get(id = profile3.id)
        self.assertTrue(hasattr(profile2,'EnergyContract') , "The energy offer should exist")
        profile3.rejectEnergyOffer(profile2.EnergyContract.id)
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        profile3 = Profile.objects.get(id = profile3.id)
        self.assertFalse(hasattr(profile2,'EnergyContract') , "The energy offer should'nt exist. It's been rejected.")
        self.assertEqual(float(profile2.capital), 100, "Player's capital should've been unaffected since the energy offer didn't go through.")
        self.assertEqual(float(profile3.capital), 100, "Player's capital should've been unaffected since the energy offer didn't go through.")
        
        
        #Testing energy offer success.
        profile2.proposeEnergyOffer(profile3.id, 3, 0.5)
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        profile3 = Profile.objects.get(id = profile3.id)
        self.assertTrue(hasattr(profile2,'EnergyContract') , "The energy offer should exist")
        profile3.acceptEnergyOffer(profile2.EnergyContract.id)
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        profile3 = Profile.objects.get(id = profile3.id)
        self.assertFalse(hasattr(profile2,'EnergyContract') , "The energy offer should'nt exist. It has been accepted.")
        self.assertEqual(float(profile2.capital), 99.5, "The energy offer should've succeeded.")
        self.assertEqual(float(profile3.capital), 100.5, "The energy offer should've succeeded.")
        self.assertEqual(float(profile2.extra_energy), 8, "The energy offer should've succeeded.")
        self.assertEqual(float(profile3.extra_energy), 2, "The energy offer should've succeeded.")
        print "Energy Deals successfully tested"
    
    def test_transport(self):
        """ Method for testing transports """
        
        profile2 = createUser(6)
        states = State.objects.exclude(pk = self.state6.id).values_list('id',flat = True)
        states = [int(i) for i in states]
        
        
        #Testing validations of transport purchase.
        try:
            profile2.buy_transport(self.transport2.id,states)
        except Exception:
            pass
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        self.assertEqual(profile2.transportcreated_set.count(),0,"Transport shouldn't have been created. (Max stops exceeded reasons)")
        self.assertEqual(profile2.capital,100.0,"No amount shouldve been deducted")
        try:
            profile2.buy_transport(self.transport1.id,states)
        except Exception:
            pass
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        self.assertEqual(profile2.transportcreated_set.count(),0,"Transport shouldn't have been created. (Invalid stop reason)")
        self.assertEqual(profile2.capital,100.0,"No amount should've been deducted")
        states = State.objects.exclude(id=self.state2.id).exclude(id=self.state6.id).values_list('id',flat = True)
        states = [int(i) for i in states]
        profile2.buy_transport(self.transport1.id,states)
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        self.assertEqual(profile2.transportcreated_set.count(),1,"Transport should have been created")
        self.assertEqual(profile2.capital,95.0,"Amount for transport should be deducted")
        profile2.buy_factory(self.prodInd1.id,self.state1.id)
        profile2.buy_factory(self.prodInd1.id,self.state2.id)
        
        
        #Testing setting transport to factories.
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        factory2 = profile2.factory_set.get(state = self.state2)
        transport = profile2.transportcreated_set.get()
        try:
            profile2.setTransport(factory2.id,transport.id)
        except Exception:
            pass
        #reload factory
        factory2 = profile2.factory_set.get(state = self.state2)
        self.assertEqual(factory2.transport, None, "Transport assigning should've failed. (Transport doesn't pass through state)")
        factory = profile2.factory_set.get(state = self.state1)
        profile2.setTransport(factory.id,transport.id)
        #reload factory, transport
        factory = profile2.factory_set.get(state = self.state1)
        transport = profile2.transportcreated_set.get()        
        self.assertTrue(bool(factory.transport), "Factory should have a transport.")
        self.assertEqual(factory.transport.id, transport.id, "The transport should've been assigned to the factory.")
        
        
        #Clearing transport off a factory.
        profile2.clearTransport(factory.id)
        #reload factory
        factory = profile2.factory_set.get(state = self.state2)
        self.assertEqual(factory.transport, None, "Factory's transport should've been cleared")
        print "Transports successfully tested"
    
    def test_research_and_industries(self):
        """ Method for testing research. """
        
        profile2 = createUser(7)
        states = State.objects.exclude(id = self.state6.id).values_list('id',flat = True)
        states = [int(i) for i in states]
        
        
        #Testing purchase of advanced transport.
        try:
            profile2.buy_transport(self.transport3.id,states)
        except Exception:
            pass
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        self.assertEqual(profile2.transportcreated_set.count(), 0, "The transport shouldn't have been created. (Transport is too advanced)")
        states = State.objects.values_list('id',flat = True)[2:]
        states = [int(i) for i in states]
        
        
        #Testing setting up transport in advanced state.
        try:
            profile2.buy_transport(self.transport2.id,states)
        except Exception:
            pass
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        self.assertEqual(profile2.transportcreated_set.count(), 0, "The transport shouldn't have been created. (State is advanced)")
        
        
        #Testing setting up factory in advanced state.
        try:
            profile2.buy_factory(self.prodInd2.id, self.state6.id)
        except Exception:
            pass
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        self.assertEqual(profile2.factory_set.count(), 0, "The factory shouldn't have been created. (State is advanced)")
        
        #Testing setting up advanced factory.
        try:
            profile2.buy_factory(self.prodInd3.id, self.state5.id)
        except Exception:
            pass
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        self.assertEqual(profile2.factory_set.count(), 0, "The factory shouldn't have been created. (Industry is advanced)")
        
        
        #Testing setting up powerplant in advanced state.
        try:
            profile2.buy_powerPlant(self.energyInd2.id, self.state6.id)
        except Exception:
            pass
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        self.assertEqual(profile2.powerplant_set.count(), 0, "The Power Plant shouldn't have been created. (State is advanced)")
        
        
        #Testing setting up advanced powerplant.
        try:
            profile2.buy_powerPlant(self.energyInd3.id, self.state5.id)
        except Exception:
            pass
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        self.assertEqual(profile2.powerplant_set.count(), 0, "The Power Plant shouldn't have been created. (Energy Industry is advanced)")
        
        
        #Testing starting and ending player's research and increasing research levels.
        profile2.startResearch()
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        self.assertTrue(hasattr(profile2, 'Research'), "The research project should've started")
        profile2.endResearch()
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        self.assertFalse(hasattr(profile2, 'Research'), "The research project should've ended")
        profile2.research_level = 4
        profile2.save()
        try:
            profile2.startResearch()
        except Exception:
            pass
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        self.assertFalse(hasattr(profile2, 'Research'), "The research project shouldnt've started because player is at maximum research level.")
        profile2.research_level = 2
        profile2.save()
        
        
        #Repeating earlier advanced purchase tests now at higher research level.
        states = State.objects.values_list('id',flat = True)[2:]
        states = [int(i) for i in states]
        profile2.buy_transport(self.transport2.id,states)
        profile2.buy_transport(self.transport3.id,states)
        profile2.buy_factory(self.prodInd3.id, self.state5.id)
        profile2.buy_factory(self.prodInd2.id, self.state6.id)
        profile2.buy_powerPlant(self.energyInd2.id, self.state6.id)
        profile2.buy_powerPlant(self.energyInd3.id, self.state5.id)
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        self.assertEqual(profile2.transportcreated_set.count(), 2, "Both Transports should've been created")
        self.assertEqual(profile2.factory_set.count(), 2, "Both Factories should've been created")
        self.assertEqual(profile2.powerplant_set.count(), 2, "Both Power Plants should've been created")
        print "Research successfully tested"
        
        
        #Start verifying factories and powerplants purchase and sale.
        #Verifying player's stats after purchase.
        self.assertEqual(float(profile2.capital), 70.0, "Capital should've been 70 Million")
        self.assertEqual(float(profile2.netWorth), 96.0, "Net worth should've been 98 Million")
        profile2.shutdownFactory(profile2.factory_set.get(type = self.prodInd2).id)
        self.assertTrue(profile2.factory_set.get(type=self.prodInd2).shut_down, "Factory should've shut down")
        profile2.restartFactory(profile2.factory_set.get(type = self.prodInd2).id)
        self.assertFalse(profile2.factory_set.get(type=self.prodInd2).shut_down, "Factory should've started")
        profile2.shutdownPowerPlant(profile2.powerplant_set.get(type = self.energyInd2).id)
        self.assertTrue(profile2.powerplant_set.get(type=self.energyInd2).shut_down, "Power plant should've shut down")
        profile2.restartPowerPlant(profile2.powerplant_set.get(type = self.energyInd2).id)
        self.assertFalse(profile2.powerplant_set.get(type=self.energyInd2).shut_down, "Power plant should've started")
        
        
        #Sell everything and verify player's stats
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        profile2.sell_transport(profile2.transportcreated_set.get(transport = self.transport2).id)
        profile2.sell_transport(profile2.transportcreated_set.get(transport = self.transport3).id)
        profile2.sell_factory(profile2.factory_set.get(type = self.prodInd2).id)
        profile2.sell_factory(profile2.factory_set.get(type = self.prodInd3).id)
        profile2.sell_powerPlant(profile2.powerplant_set.get(type = self.energyInd2).id)
        profile2.sell_powerPlant(profile2.powerplant_set.get(type = self.energyInd3).id)
        
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        
        self.assertEqual(profile2.transportcreated_set.count(), 0, "Both Transports should've been sold")
        self.assertEqual(profile2.factory_set.count(), 0, "Both Factories should've been sold")
        self.assertEqual(profile2.powerplant_set.count(), 0, "Both Power Plants should've been sold")
        
        self.assertEqual(float(profile2.capital), 94.0, "Capital should've been 100 Million")
        self.assertEqual(float(profile2.netWorth), 94.0, "Net worth should've been 100 Million")
        
        print "Factories and powerplants successfully tested"
    
    def test_cron(self):
        """A variable testing method. For immediate and custom use. 
        Also checks database queries for various processes (purchase, sale ,assignment)
        """
        
        profile2 = createUser(8)
        profile2.research_level = 2
        profile2.save()
        
        startMeasure()
        
        states = State.objects.exclude(id__in = [self.state1.id,self.state2.id]).values_list('id',flat = True)
        states = [int(i) for i in states]
        
        a = len(connection.queries)
        
        states2 = list(states)
        states2.remove(int(self.state5.id))
        
        profile2.buy_transport(self.transport2.id,states)
        profile2.buy_transport(self.transport3.id,states2)
        profile2.buy_factory(self.prodInd3.id, self.state5.id)
        profile2.buy_factory(self.prodInd2.id, self.state6.id)
        profile2.buy_powerPlant(self.energyInd2.id, self.state6.id)
        profile2.buy_powerPlant(self.energyInd3.id, self.state5.id)
        
        b = len(connection.queries)
        
        transport = profile2.transportcreated_set.get(transport = self.transport2)
        factory = profile2.factory_set.get(state = self.state5)
        profile2.setTransport(factory.id,transport.id)
        
        c = len(connection.queries)
        
        factories = Factory.objects.filter(transport__states__in = [self.state3])
        
        d = len(connection.queries)
        
        endMeasure()
