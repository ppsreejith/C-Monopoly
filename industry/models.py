from django.db import models
from django.core.exceptions import ValidationError
from calamity.models import checkStateAvailable

# Create your models here.

#This is an abstract class
class AbstractIndustry(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    states = models.ManyToManyField('govt.State')
    carbon_per_unit = models.DecimalField(max_digits = 10, decimal_places = 5)
    initial_cost = models.DecimalField(max_digits = 10, decimal_places = 2, help_text = "In Millions")
    maintenance_cost = models.DecimalField(max_digits = 10, decimal_places = 2, help_text = "In Thousands")
    research_level = models.PositiveIntegerField(help_text="Typically a small integer.") 
    annual_value_decrease = models.DecimalField(max_digits = 5, decimal_places = 2, help_text="Rate of value loss, yearly.")
    class Meta:
        abstract = True

class ProductIndustry(AbstractIndustry):
    cost_price = models.DecimalField(max_digits = 10, decimal_places = 5, help_text = "In Thousands")
    initial_energy = models.PositiveIntegerField(help_text="In number of units of energy (Integer)")
    maintenance_energy = models.PositiveIntegerField(help_text="In number of units of energy (Integer)")
    energy_per_unit = models.DecimalField(max_digits = 10, decimal_places = 5)
    unit = models.CharField(max_length = 50)
    def __unicode__(self):
        return self.name

#Created Product Industry
class Factory(models.Model):
    type = models.ForeignKey(ProductIndustry)
    state = models.ForeignKey('govt.State')
    transport = models.ForeignKey('transport.TransportCreated', help_text = "Transport Used to export", null = True, blank = True)
    player = models.ForeignKey('player.Player')
    selling_price = models.DecimalField(max_digits = 10, decimal_places = 5, help_text="In thousands")
    actual_value = models.DecimalField(max_digits = 10, decimal_places = 2, help_text = "In Millions")
    products_last_month = models.PositiveIntegerField()
    shut_down = models.BooleanField()
    def __unicode__(self):
        return str(self.type) + " by " + str(self.player)
    def clean(self):
        checkStateAvailable(self)
        transport_check(self)

def transport_check(self):
    if hasattr(self , 'transport') and not(self.transport == None):
        if self.state not in self.transport.states.all():
            raise ValidationError("Transport does not pass through state.")
        if self.transport.player != self.player:
            raise ValidationError("You cant use someone else's transport")