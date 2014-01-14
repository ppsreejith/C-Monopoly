from actions.models import Profile
from industry.models import ProductIndustry, Factory
from govt.models import State
from energy.models import EnergyIndustry
from calamity.models import Calamity
from transport.models import Transport, TransportCreated
from django.db import connection
from django.conf import settings
from django.contrib.auth.models import User

"""
Created by ppsreejith
Contains functions for creating game data.
"""

def createUser(no, extra_energy = 5, energy_capacity =30):
    """Creates a user and profile class according to supplied arguments.
    
    Args:
        no - A number to uniqely identify constant.
        extra_energy - Extra energy of user to assign. Default value 5
        energy_capacity - Energy Capacity of player. Default value 30
    
    Returns:
        An new instance of profile model.
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
    
    Returns:
        Returns reference to the list connection.queries which can be used
        to note the number of connections made to the database.
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
    
    Returns:
        A new instance of ProductIndustry model.
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
    
    Returns:
        A new instance of EnergyIndustry model.
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
    
    Returns:
        A new instance of Calamity model.
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

    Returns:
        A new instance of State model.
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

    Returns:
        A new instance of Transport model.
    """
    
    transport = Transport(name = name, research_level = research_level, energy_rate = energy_rate,
                          max_stops = max_stops, stopping_cost = stopping_cost, travel_rate = travel_rate,
                          initial_cost = initial_cost, carbon_cost_rate = carbon_cost_rate)
    transport.save()
    transport.states.add(*states)
    transport.save()
    return transport
