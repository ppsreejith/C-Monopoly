from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
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

class LoansCreated(models.Model):
    player = models.ForeignKey('player.Player')
    amount = models.DecimalField(max_digits = 10, decimal_places = 2, help_text = "In millions")
    time_remaining = models.PositiveIntegerField(help_text = "In number of months")
    mortaged_industries = models.ManyToManyField('industry.Factory')
    def __unicode__(self):
        return str(self.amount * self.time_remaining) + " million Rs by " + str(self.player)
    class Meta:
        verbose_name_plural = "Loans"
        verbose_name = "Loan"
    def update(self):
        if self.player.capital > self.amount + 30:
            self.player.capital -= self.amount
            self.player.save()
            if self.time_remaining <= 1:
                self.delete()
            else:
                self.time_remaining -= 1
                self.save()
        else:
            if self.time_remaining <= 1:
                self.mortaged_industries.all().delete()
                self.delete()
            else:
                self.amount *= self.time_remaining/(self.time_remaining-1)
                self.time_remaining -= 1
                self.player.loan_defaults += 1
                self.save()

class AquireRecord(models.Model):
    from_player = models.ForeignKey('player.Player', related_name = 'SellRecord')
    to_player = models.ForeignKey('player.Player', related_name = 'BuyRecord')
    amount = models.DecimalField(max_digits = 15, decimal_places = 5, help_text = "In millions")
    time = models.DateTimeField('Date and Time')
    def __unicode__(self):
        return str(self.amount) + " Rs for " + str(self.to_player) + " by " + str(self.from_player)
    def clean(self):
        two_different_players(self)

class EnergyDeal(models.Model):
    from_player = models.ForeignKey('player.Player', related_name = 'SoldEnergy')
    to_player = models.ForeignKey('player.Player', related_name = 'BoughtEnergy')
    amount_energy = models.PositiveIntegerField(help_text = "Number of units of energy (Integer)")
    time = models.DateTimeField('Date and Time')
    cost = models.DecimalField(max_digits = 15, decimal_places = 5, help_text = "In millions")
    def __unicode__(self):
        return str(self.amount) + " Rs for " + str(self.to_player) + " by " + str(self.from_player)
    def clean(self):
        two_different_players(self)

#Only one should be instantiated
class GlobalConstants(models.Model):
    carbon_buying_price = models.DecimalField(max_digits = 9, decimal_places = 2, help_text = "price at which carbon sold to govt" ) #price at which carbon sold to govt
    carbon_selling_price = models.DecimalField(max_digits = 9, decimal_places = 2, help_text = "price at which govt sells carbon") #price at which govt sells carbon
    energy_buying_price = models.DecimalField(max_digits = 9, decimal_places = 2, help_text = "price at which energy sold to govt") #price at which energy sold to govt
    energy_selling_price = models.DecimalField(max_digits = 9, decimal_places = 2, help_text = "price at which govt sells energy") #price at which govt sells energy
    tax_rate = models.DecimalField(max_digits = 5, decimal_places = 2, help_text="Percentage of revenue as tax.") #revenue tax
    loan_interest_rate = models.DecimalField(max_digits = 5, decimal_places = 2, help_text="Percentage of loan as interest") #Loan Interest Rate
    vehicle_variable_limit = models.DecimalField(max_digits = 5, decimal_places = 2, help_text="Maximum deviation in percentage.") #Variable Vehicle Cost Limit.
    max_research_level = models.PositiveIntegerField(help_text="Maximum Research Level (Integer)") #Maximum Research Level
    initial_research_time = models.PositiveIntegerField(help_text = "In number of months (Integer)") # will be multiplied by research level
    monthly_research_cost = models.DecimalField(max_digits = 9, decimal_places = 2, help_text = "In cost per month, in millions") # will be multiplied by research level
    def __unicode__(self):
        return "Global Constants"
    #Only one global constants instance necessary
    def clean(self):
        validate_only_one_instance(self)
    class Meta:
        verbose_name = verbose_name_plural = "Global Constants"

#Check if only one instance
def validate_only_one_instance(obj):
    model = obj.__class__
    if model.objects.count() > 0 and  obj.id != model.objects.get().id:
        raise ValidationError("Can only create 1 %s instance" % model.__name__)

#Check if two different players
def two_different_players(obj):
    #foreign key validation
    if not hasattr(obj, 'from_player') or not hasattr(obj, 'to_player') or obj.from_player == obj.to_player:
        raise ValidationError("Two different players needed.")

#selling prices should be lesser than buying price.
def check_price(obj):
    if obj.carbon_buying_price > obj.carbon_selling_price:
        raise ValidationError("Carbon buying price bigger than carbon selling price")
    if obj.energy_buying_price > obj.energy_selling_price:
        raise ValidationError("Energy buying price bigger than carbon selling price")

#Check if factories not already under loan
def check_factories(mortaged_industries,pk,amount,time_remaining,player):
    all_industries = mortaged_industries.all()
    if not LoansCreated.objects.filter(mortaged_industries__in = all_industries).distinct().exclude(pk = pk).exists():
        if all_industries.aggregate(sum = models.Sum('actual_value'))['sum'] < amount*time_remaining:
            raise ValidationError("Loan amount requested is too large.")
        if all_industries.exclude(player = player).exists():
            raise ValidationError("You can only mortage your own industries")
    else:
        raise ValidationError("You can't mortage a factory twice!")