from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

#The class for every players stats.
class Player(models.Model):
    monthly_carbon_total = models.IntegerField()
    name = models.CharField(max_length = 100, unique = True)
    net_worth = models.DecimalField(max_digits = 15, decimal_places = 2, help_text="In millions")
    capital = models.DecimalField(max_digits = 15, decimal_places = 2, help_text="In millions")
    research_level = models.PositiveIntegerField(help_text="Typically a small number (Integer)")
    brand = models.DecimalField(max_digits = 4, decimal_places = 2, help_text="Typically a small number")
    extra_energy = models.PositiveIntegerField(help_text="Typically a small number (Integer)")
    energy_capacity = models.PositiveIntegerField(help_text="Typically a small number (Integer)")
    loan_defaults = models.IntegerField(help_text="Typically a small number (Integer)")
    suspended = models.BooleanField(default = False)
    shutdown = models.BooleanField(default = False)
    user_login_id = models.PositiveIntegerField(unique = True)
    def __unicode__(self):
        return self.name

class ResearchProject(models.Model):
    player = models.ForeignKey(Player)
    time_remaining = models.PositiveIntegerField(help_text = "Months remaining (Integer)")
    def __unicode__(self):
        return str(self.time_remaining) + " month(s) to next level for " + str(self.player)
    def clean(self):
        validate_only_one_instance(self)

#Check if only one instance per player
def validate_only_one_instance(obj):
    model = obj.__class__
    if not hasattr(obj , 'player'):
        raise ValidationError("Please fill all fields")
    if model.objects.filter(player = obj.player).count() > 0 and  obj.id != model.objects.get(player = obj.player).id:
        raise ValidationError("A player can only start one research project at a time")