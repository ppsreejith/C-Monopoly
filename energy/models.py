from django.db import models
from industry.models import AbstractIndustry
from calamity.models import checkStateAvailable
# Create your models here.

#see industry.models.Industry for more general properties.
class EnergyIndustry(AbstractIndustry):
    output = models.PositiveIntegerField(help_text = "Number of units of energy (Integer)")
    def __unicode__(self):
        return self.name

#Created Energy Industry    
class PowerPlant(models.Model):
    type = models.ForeignKey(EnergyIndustry)
    player = models.ForeignKey('player.Player')
    state = models.ForeignKey('govt.State')
    actual_value = models.DecimalField(max_digits = 9, decimal_places = 2, help_text = "In Millions")
    def __unicode__(self):
        return str(self.type) + " by " + str(self.player)
    def clean(self):
        checkStateAvailable(self)
    def update(self):#yearly
        self.actual_value *= (100 - self.type.annual_value_decrease)/100
        self.save()