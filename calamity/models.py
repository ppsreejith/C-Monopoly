from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
# Create your models here.

class Calamity(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    states = models.ManyToManyField('govt.State')
    severity = models.PositiveIntegerField(validators = [MinValueValidator(0),
                                                         MaxValueValidator(100)]
                                           , help_text = "An Integer from 1 to 100")
    probability_number = models.PositiveIntegerField(help_text = "An Integer from 1 to 100")
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Calamities"

class CalamityOccurence(models.Model):
    type = models.ForeignKey(Calamity)
    state = models.OneToOneField('govt.State')
    time_remaining = models.PositiveIntegerField(help_text = "Number of months remaining (Integer)")
    def __unicode__(self):
        return str(self.type) + " in " + str(self.state)
    def clean(self):
        checkStateAvailable(self)
    def monthlyUpdate(self):
        if self.time_remaining == 0:
            self.delete()
        else:
            self.time_remaining -= 1
            self.save()

def checkStateAvailable(obj):
    if not hasattr(obj, 'state') or not hasattr(obj, 'type'):
        raise ValidationError("Fill all necessary fields")
    states_list = list(obj.type.states.all())
    if obj.state not in states_list:
        raise ValidationError(str(obj.type) + " not available in " + str(obj.state))
    if hasattr(obj,'player'):
        if obj.player.research_level < obj.state.research_level:
            raise ValidationError("You do not have enough technological capability to access this state.")