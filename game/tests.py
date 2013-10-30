from django.test import TestCase
from game.models import GlobalConstants
from django.contrib.auth.models import User
from django.db import IntegrityError
from actions.models import Profile
from industry.models import ProductIndustry
from govt.models import State
from energy.models import EnergyIndustry
from calamity.models import Calamity
from transport.models import Transport
from django.core.exceptions import ValidationError

class ModelsTestCase(TestCase):

    def createUser(self,no):
        user = User.objects.create_user("testuser%d"%no, "testuser%d@gmail.com"%no, "password")
        profile = Profile(user_login_id = "1665%d"%no, user = user)
        profile.full_clean()
        profile.save()
        return profile
    
    def createProductIndustry(self,name = "Coconut",maintenance_energy = 4,energy_per_unit = 0.5,
                              unit = "Pieces",research_level = 1,annual_value_decrease = 5.4,cost_price = 1,
                              maintenance_cost = 40,initial_cost = 5,carbon_per_unit = 0.003,states = [1,2,3,4]):
        industry = ProductIndustry(name = name,maintenance_energy = maintenance_energy,cost_price = cost_price,
                                   energy_per_unit = energy_per_unit,unit = unit,research_level = research_level,
                                   annual_value_decrease = annual_value_decrease,maintenance_cost = maintenance_cost,
                                   initial_cost = initial_cost,carbon_per_unit = carbon_per_unit)
        industry.save()
        industry.states.add(*states)
        return industry
    
    def createEnergyIndustry(self,name = "Coal",research_level = 1,output = 5,
                             annual_value_decrease = 5.4,maintenance_cost = 40,initial_cost = 5,
                             carbon_per_unit = 0.003,states = [1,2,3,4]):
        industry = EnergyIndustry(name = name,research_level = research_level,output = output,
                                   annual_value_decrease = annual_value_decrease,maintenance_cost = maintenance_cost,
                                   initial_cost = initial_cost,carbon_per_unit = carbon_per_unit)
        industry.save()
        industry.states.add(*states)
        return industry
        
    def createCalamity(self, name = "Tornado",severity = 80, probability_number = 0.02, states = [2,3,4,5]):
        calamity = Calamity(name = name, probability_number = probability_number, severity = severity)
        calamity.save()
        calamity.states.add(*states)
        return calamity
    
    def createState(self, name = "Telengana",coordx = 6, coordy = 4,population = 34.5,
                    research_level = 1, capacity = 30, energy_plant_capacity = 20, income = 30.4, 
                    growth_rate = 4.5, income_growth_rate = 4.5):
        state = State(name = name, coordx = coordx, coordy = coordy, population = population,
                            research_level = research_level, capacity = capacity,growth_rate = growth_rate,
                            energy_plant_capacity = energy_plant_capacity, income = income,
                            income_growth_rate = income_growth_rate)
        state.save()
        return state
    
    def createTransport(self, name = "Train",research_level = 1,energy_rate=0.2,
                        max_stops = 6,stopping_cost = 40,travel_rate = 30,
                        initial_cost = 5,carbon_cost_rate = 0.003,states = [1,2,3,4]):
        transport = Transport(name = name, research_level = research_level, energy_rate = energy_rate,
                              max_stops = max_stops, stopping_cost = stopping_cost, travel_rate = travel_rate,
                              initial_cost = initial_cost, carbon_cost_rate = carbon_cost_rate)
        transport.save()
        transport.states.add(*states)
        return transport
    
    def setUp(self):
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
                                          initial_capital = 100)
        globalConstants.full_clean()
        globalConstants.save()
        
        #Create a default player
        self.profile = self.createUser(1)
        s1 = self.state1 = self.createState()
        s2 = self.state2 = self.createState(name = "Bihar",coordx = 10, coordy = 20)
        s3 = self.state3 = self.createState(name = "Rajasthan",coordx = 10, coordy = 30)
        s4 = self.state4 = self.createState(name = "Andhra Pradesh",coordx = 15, coordy = 20)
        s5 = self.state5 = self.createState(name = "Kashmir",coordx = 10, coordy = 11)
        self.prodInd1 = self.createProductIndustry(states = [s1,s2,s3,s4])
        self.prodInd2 = self.createProductIndustry(name = "Rubber",states = [s1,s2,s4,s5])
        self.energyInd1 = self.createEnergyIndustry(states = [s1,s2,s3,s4])
        self.energyInd2 = self.createEnergyIndustry(name = "Biofuel",states = [s2,s3,s4,s5])
        self.transport1 = self.createTransport(states = [s1,s3,s4,s5])
        self.transport2 = self.createTransport(name = "Road",states = [s1,s2,s4,s5])
        self.calamity1 = self.createCalamity(states = [s2,s3,s4,s5])
        self.calamity2 = self.createCalamity(name = "Hurricane",states = [s1,s2,s3,s5])
    
    def test_player(self):
        self.assertEqual(self.profile.capital, GlobalConstants.objects.get().initial_capital, "Default capital is wrong")
        self.assertEqual(self.profile.net_worth, GlobalConstants.objects.get().initial_capital, "Default net worth is wrong")
        
        #Test if two seperate players can be made with same values
        try:
            profile2 = self.createUser(2)
            profile3 = self.createUser(2)
        except IntegrityError:
            self.assertEqual(True, True, "Error: Two profiles were made with the same username.")
    
    def test_loan_scenario(self):
        profile2 = self.createUser(3)
        profile2.buy_factory(self.prodInd1.id,self.state1.id)
        profile2.buy_factory(self.prodInd1.id,self.state2.id)
        try:
            profile2.buy_factory(self.prodInd2.id,self.state3.id)
        except ValidationError:
            pass
        profile2.buy_factory(self.prodInd2.id,self.state4.id)
        
        values = profile2.factory_set.values_list('id', flat=True)
        values = [int(i) for i in values]
        
        try:
            profile2.takeLoan(100,12,values)
        except Exception:
            pass
        profile2.takeLoan(5,12,values[0:2])
        try:
            self.profile.takeLoan(3,12,values[2])
        except Exception:
            pass
        
        self.assertEqual(profile2.factory_set.count(),3,"profile2 must have only 3 factories")
        
        #profile2's loan must be 5 million
        self.assertEqual(float(profile2.Loan.amount)*float(profile2.Loan.time_remaining), 
                         5*(100.0 + float(GlobalConstants.objects.get().loan_interest_rate))/100, 
                         "Loan amount is incorrect")
        
        #profile must not have a loan
        self.assertFalse(hasattr(self.profile,'Loan'),"Self.player's loan is invalid")
    
    def test_energyDeal(self):
        profile2 = self.createUser(4)
        profile3 = self.createUser(5)
        
        try:
            profile2.proposeEnergyOffer(profile3.id, 3, 0.5)
        except ValidationError:
            pass
        
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        profile3 = Profile.objects.get(id = profile3.id)
        
        self.assertFalse(hasattr(profile2,'EnergyContract') , "The energy offer should've expired")
        profile3.setSellingEnergy(True) #Available for selling now
        
        profile2.proposeEnergyOffer(profile3.id, 3, 0.5)
        
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        profile3 = Profile.objects.get(id = profile3.id)
        
        self.assertTrue(hasattr(profile2,'EnergyContract') , "The energy offer should exist")
        
        #Reject offer
        profile3.rejectEnergyOffer(profile2.EnergyContract.id)
        
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        profile3 = Profile.objects.get(id = profile3.id)
        
        self.assertFalse(hasattr(profile2,'EnergyContract') , "The energy offer should've expired")
        
        self.assertEqual(float(profile2.capital), 100, "The energy offer should've failed")
        self.assertEqual(float(profile3.capital), 100, "The energy offer should've failed")
        
        profile2.proposeEnergyOffer(profile3.id, 3, 0.5)
        
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        profile3 = Profile.objects.get(id = profile3.id)
        
        self.assertTrue(hasattr(profile2,'EnergyContract') , "The energy offer should exist")
        
        #Accept offer
        profile3.acceptEnergyOffer(profile2.EnergyContract.id)
        
        #Reload models
        profile2 = Profile.objects.get(id = profile2.id)
        profile3 = Profile.objects.get(id = profile3.id)
        
        self.assertFalse(hasattr(profile2,'EnergyContract') , "The energy offer should've expired")
        
        self.assertEqual(float(profile2.capital), 99.5, "The energy offer failed")
        self.assertEqual(float(profile3.capital), 100.5, "TThe energy offer failed")
        self.assertEqual(float(profile2.extra_energy), 8, "The energy offer failed")
        self.assertEqual(float(profile3.extra_energy), 2, "The energy offer failed")
    
    def test_buy_transport(self):
        profile2 = self.createUser(6)
        #profile2.buy_transport(self.transport1.id,State.objects.values_list('id',flat = True))
        