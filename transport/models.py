from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Transport(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    research_level = models.PositiveIntegerField(help_text="Typically a small number (Integer)")
    states = models.ManyToManyField('govt.State', help_text = "Available states")
    minimum_cost = models.DecimalField(max_digits = 9, decimal_places = 2, help_text="In thousands")
    stopping_cost = models.DecimalField(max_digits = 9, decimal_places = 2, help_text="In thousands")
    travel_rate = models.DecimalField(max_digits = 9, decimal_places = 2, help_text="In thousands")
    max_stops = models.PositiveIntegerField(help_text="Typically a small number (Integer)")
    carbon_cost_rate = models.DecimalField(max_digits = 9, decimal_places = 2, help_text = "Carbon cost per distance")
    def __unicode__(self):
        return self.name

class TransportCreated(models.Model):
    transport = models.ForeignKey(Transport)
    states = models.ManyToManyField('govt.State',help_text = "Available Stops")
    player = models.ForeignKey('player.Player')
    def __unicode__(self):
        return str(self.transport) + " by " + str(self.player)
    class Meta:
        verbose_name = "Created Transport"

def check_stops(states, transport):
    if states.count() > transport.max_stops:
        raise ValidationError("Maximum number of stops exceeded")
    elif set(states.all()) - set(transport.states.all()):
        raise ValidationError("Invalid stops")

def check_no_states(states):
    if states.count() < 3:
        raise ValidationError("Need more states")