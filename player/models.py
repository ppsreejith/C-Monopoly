from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from game.models import GlobalConstants

#The class for every players stats.
class Player(models.Model):
    monthly_carbon_total = models.IntegerField(help_text = "In Integers.", default = 0)
    last_month_total = models.IntegerField(help_text = "In Integers.", default = 0)
    netWorth = models.DecimalField(max_digits = 15, decimal_places = 2, help_text = "In millions", default = lambda:GlobalConstants.objects.get().initial_capital)
    capital = models.DecimalField(max_digits = 15, decimal_places = 2, help_text = "In millions", default = lambda:GlobalConstants.objects.get().initial_capital)
    research_level = models.PositiveIntegerField(help_text = "Typically a small number (Integer)", default = 1)
    brand = models.DecimalField(max_digits = 4, decimal_places = 2, help_text = "Typically a small number", default = 5)#Goodwill among the people
    extra_energy = models.DecimalField(max_digits = 10, decimal_places = 5, help_text = "Typically a small number (Integer)", default = 50)
    energy_capacity = models.PositiveIntegerField(help_text = "Typically a small number (Integer)", default = 300)
    loan_defaults = models.IntegerField(help_text = "Typically a small number (Integer)", default = 0)
    suspended = models.BooleanField(default = False)
    selling_energy = models.BooleanField(default = False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    rank = models.PositiveIntegerField(default = lambda: (Player.objects.count()+1) )
    join_date = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):
        return self.user.username
 
class LogBook(models.Model):
    player = models.ForeignKey(Player)
    datetime = models.DateTimeField(auto_now_add = True)
    message = models.CharField(max_length = 150)

class ResearchProject(models.Model):
    player = models.OneToOneField(Player, related_name = 'Research')
    time_remaining = models.PositiveIntegerField(help_text = "Months remaining (Integer)", default = lambda:GlobalConstants.objects.get().initial_research_time)#
    def monthlyUpdate(self):
        monthly_cost = GlobalConstants.objects.get().monthly_research_cost*self.player.research_level #
        if self.player.capital > monthly_cost + 30:
            self.player.capital = self.player.capital - monthly_cost
            LogBook.objects.create(player = self.player, message = "Research Project cost Rs. %.2f Million."%monthly_cost)
            if self.time_remaining > 1:
                self.time_remaining -= 1
                self.player.save()
                self.save()
            else:
                self.player.research_level = self.player.research_level + 1
                self.player.save()
                self.delete()
        else:
            LogBook.objects.create(player = self.player, message = "Research Project cancelled due to lack of capital.")
            self.delete()
    def __unicode__(self):
        return str(self.time_remaining) + " month(s) to next level for " + str(self.player)
    def clean(self):
        if self.player.research_level == GlobalConstants.objects.get().max_research_level:#
            raise ValidationError("Maximum research level reached.")