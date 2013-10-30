from django.db import models
from django.core.exceptions import ValidationError
from player.models import Player
from govt.models import State

# Create your models here.
class Transport(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    research_level = models.PositiveIntegerField(help_text="Typically a small number (Integer)")
    states = models.ManyToManyField(State, help_text = "Available states")
    initial_cost = models.DecimalField(max_digits = 9, decimal_places = 2, help_text="In Millions")
    stopping_cost = models.DecimalField(max_digits = 9, decimal_places = 2, help_text="In thousands")
    travel_rate = models.DecimalField(max_digits = 9, decimal_places = 2, help_text="In thousands. Cost per unit distance.")
    max_stops = models.PositiveIntegerField(help_text="Typically a small number (Integer)")
    carbon_cost_rate = models.DecimalField(max_digits = 9, decimal_places = 2, help_text = "Carbon cost per unit distance.")
    energy_rate = models.DecimalField(max_digits = 9, decimal_places = 2, help_text = "Energy units per unit distance.")
    def __unicode__(self):
        return self.name

class TransportCreated(models.Model):
    transport = models.ForeignKey(Transport)
    states = models.ManyToManyField(State,help_text = "Available Stops")
    player = models.ForeignKey(Player)
    def __unicode__(self):
        return str(self.transport) + " by " + str(self.player)
    class Meta:
        verbose_name = "Created Transport"

def check_stops(states, transport):
    check_no_states(states)
    if states.count() > transport.max_stops:
        raise ValidationError("Maximum number of stops exceeded")
    elif set(states.all()) - set(transport.states.all()):
        raise ValidationError("Invalid stops")

def check_no_states(states):
    if states.count() < 3:
        raise ValidationError("Need more states")

def check_player(transport,player):
    if player.research_level < transport.research_level:
        raise ValidationError("You are not qualified enough to build this transport.")
    if player.transportcreated_set.count() > 3:
        raise ValidationError("You have reached the maximum number of transports possible.")
    check_commodity(transport,player)

def check_commodity(commodity, player):
    if commodity.initial_cost > player.capital - 30:
        raise ValidationError("This %s is too expensive for you."%str(commodity))