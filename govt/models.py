from django.db.models import F
from django.db import models
from django.core.exceptions import ValidationError
from player.models import LogBook, Player
from decimal import Decimal

#State model
class State(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    coordx = models.IntegerField(help_text="X Co-ordinate (Integer)")
    coordy = models.IntegerField(help_text="Y Co-ordinate (Integer)")
    population = models.DecimalField(max_digits = 9, decimal_places = 2, help_text = "In millions")
    research_level = models.PositiveIntegerField(help_text = "Typically a small Integer")
    capacity = models.PositiveIntegerField(help_text = "Typically a small Integer")
    energy_plant_capacity = models.PositiveIntegerField(help_text = "Typically a small Integer")
    income = models.DecimalField(max_digits = 9, decimal_places = 2, help_text = "In thousands")
    growth_rate = models.DecimalField(max_digits = 9, decimal_places = 4, help_text = "Yearly Population Growth Percentage")
    income_growth_rate = models.DecimalField(max_digits = 9, decimal_places = 4, help_text = "Yearly Income Growth Percentage")
    class Meta:
        unique_together = ('coordx','coordy',)
    def __unicode__(self):
        return self.name
    def annualUpdate(self):
        self.income = F('income')*(Decimal(100)+F('income_growth_rate'))/Decimal(100)
        self.population = F('population')*(Decimal(100)+F('growth_rate'))/Decimal(100)

#Acquisition deal between players
class AquireRecord(models.Model):
    to_player = models.OneToOneField(Player, related_name = 'Offer') #Checks for IntegrityError to display acquisition failed.
    from_player = models.OneToOneField(Player, related_name = 'Acquisition')
    amount = models.DecimalField(max_digits = 15, decimal_places = 5, help_text = "In millions")
    def __unicode__(self):
        return str(self.amount) + " Rs for " + str(self.to_player) + " by " + str(self.from_player)
    def clean(self):
        two_different_players(self)
        check_players_worth(self)
    def failed(self):
        LogBook.objects.create(player = self.to_player, message = "Acquisition Rejected.")
        self.delete()

#Energy deal between players.
#Energy transferred from `from_player` to `to_player`
class EnergyDeal(models.Model):
    from_player = models.ForeignKey(Player, related_name = 'EnergyOffer')
    to_player = models.OneToOneField(Player, related_name = 'EnergyContract')
    amount_energy = models.PositiveIntegerField(help_text = "Number of units of energy (Integer)")
    cost = models.DecimalField(max_digits = 15, decimal_places = 5, help_text = "In millions")
    def __unicode__(self):
        return str(self.cost) + " Rs for " + str(self.to_player) + " by " + str(self.from_player)
    def clean(self):
        two_different_players(self)
        check_players_amounts(self)
    def accept(self):
        check_players_amounts(self)
        self.from_player.capital = F('capital') + float(self.cost)
        self.to_player.capital = F('capital') - float(self.cost)
        self.from_player.extra_energy = F('extra_energy') - float(self.amount_energy)
        self.to_player.extra_energy = F('extra_energy') + float(self.amount_energy)
        self.from_player.save()
        self.to_player.save()
        LogBook.objects.create(player = self.to_player, message = "%.2f Million spent in buying energy."%self.cost)
        self.delete()
    def reject(self):
        LogBook.objects.create(player = self.to_player, message = "Energy deal rejected.")
        self.delete()

#Check if two different players
def two_different_players(obj):
    #foreign key validation
    if not hasattr(obj, 'from_player') or not hasattr(obj, 'to_player') or obj.from_player == obj.to_player:
        raise ValidationError("Two different players needed.")

#check on the players constraints
def check_players_worth(obj):
    if float(obj.to_player.netWorth) < 500.0:
        raise ValidationError("Cannot buy Industry worth less than 500 Million")
    if float(obj.from_player.capital) < float(obj.amount) + 30.0:
        raise ValidationError("You cannot afford it")
    if obj.amount < obj.to_player.netWorth - obj.to_player.capital:
        raise ValidationError("You cannot buy it for less than what he is worth.")
    if hasattr(obj.to_player, 'Loan'):
        raise ValidationError("The user still has loans left to pay.")

def check_players_amounts(obj):
    if not obj.from_player.selling_energy:
        raise ValidationError("Energy not for sale")
    if obj.from_player.extra_energy < obj.amount_energy:
        raise ValidationError("Not enough energy to sell.")
    if float(obj.to_player.capital) < float(obj.cost) + 30:
        raise ValidationError("You can't afford it.")

#selling prices should be lesser than buying price.
def check_price(obj):
    if obj.carbon_buying_price > obj.carbon_selling_price:
        raise ValidationError("Carbon buying price bigger than carbon selling price")
    if obj.energy_buying_price > obj.energy_selling_price:
        raise ValidationError("Energy buying price bigger than carbon selling price")

#Check if factories not already under loan
def check_factories(mortaged_industries,amount,time_remaining,player):
    if mortaged_industries.exclude(player = player).exists():
        raise ValidationError("You can only mortage your own industries")
    if mortaged_industries.aggregate(sum = models.Sum('actual_value'))['sum'] < amount*time_remaining:
        raise ValidationError("Loan amount requested is too large.")