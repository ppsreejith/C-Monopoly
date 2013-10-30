from django.db.models import F
from django.db import models
from django.core.exceptions import ValidationError
from calamity.models import checkStateAvailable
from transport.models import check_commodity, TransportCreated
from player.models import Player, LogBook
from govt.models import State

#This is an abstract class
class AbstractIndustry(models.Model):
    name = models.CharField(max_length = 100, unique = True)
    states = models.ManyToManyField(State)
    carbon_per_unit = models.DecimalField(max_digits = 10, decimal_places = 5)
    initial_cost = models.DecimalField(max_digits = 10, decimal_places = 2, help_text = "In Millions")
    maintenance_cost = models.DecimalField(max_digits = 10, decimal_places = 2, help_text = "In Thousands")
    research_level = models.PositiveIntegerField(help_text="Typically a small integer.")
    annual_value_decrease = models.DecimalField(max_digits = 5, decimal_places = 2, help_text="Rate of value loss, yearly.")
    class Meta:
        abstract = True

class ProductIndustry(AbstractIndustry):
    cost_price = models.DecimalField(max_digits = 10, decimal_places = 5, help_text = "In Thousands")
    maintenance_energy = models.PositiveIntegerField(help_text="In number of units of energy (Integer)")
    energy_per_unit = models.DecimalField(max_digits = 10, decimal_places = 5)
    unit = models.CharField(max_length = 50)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Product Industries"

#Created Product Industry
class Factory(models.Model):
    type = models.ForeignKey(ProductIndustry)
    state = models.ForeignKey(State)
    transport = models.ForeignKey(TransportCreated, help_text = "Transport Used to export", null = True, blank = True)
    player = models.ForeignKey(Player)
    selling_price = models.DecimalField(max_digits = 10, decimal_places = 5, help_text="In thousands")
    actual_value = models.DecimalField(max_digits = 10, decimal_places = 2, help_text = "In Millions")
    products_last_month = models.PositiveIntegerField(default = 0)
    shut_down = models.BooleanField(default = False)
    class Meta:
        verbose_name_plural = "Factories"
    
    def __unicode__(self):
        return str(self.type) + " by " + str(self.player)
    def clean(self):
        checkStateAvailable(self)
        transport_check(self)
        check_commodity(self.type, self.player)
        check_player_research_level(self)
    
    def annualUpdate(self):#yearly
        self.actual_value = F('actual_value') * (100 - self.type.annual_value_decrease)/100
        self.save()
    
    def setSellingPrice(self, new_sp):
        if new_sp < self.cost_price:
            raise ValidationError("Selling price cannot be lower than cost price.")
        else:
            self.selling_price = new_sp
            self.save()
    
    def setTransport(self, transportcreated):
        if transportcreated == None:
            self.transport = None
        else:
            self.transport = transportcreated
            transport_check(self)
        self.save()
    
    def clearTransport(self):
        self.transport = None
        self.save()

#An existing loan
class LoansCreated(models.Model):
    player = models.OneToOneField(Player, related_name="Loan")
    amount = models.DecimalField(max_digits = 10, decimal_places = 2, help_text = "In millions")
    time_remaining = models.PositiveIntegerField(help_text = "In number of months")
    mortaged_industries = models.ManyToManyField(Factory)
    def __unicode__(self):
        return str(self.amount * self.time_remaining) + " million Rs by " + str(self.player)
    class Meta:
        verbose_name_plural = "Loans"
        verbose_name = "Loan"
    
    def payBack(self,amount):
        player = self.player
        if amount > player.capital - 30:
            raise ValidationError("You don't have that much money.")
        if amount >= self.amount*self.time_remaining:
            amount = self.amount*self.time_remaining
            player.capital = F('capital') - amount
            self.delete()
        else:
            player.capital = F('capital') - amount
            self.amount = F('amount') - float(amount)/self.time_remaining
            self.save()
        player.save()
        LogBook.objects.create(player = self.player, message = "%.2f Million pay back loan amount."%amount)
    
    def monthlyUpdate(self):
        if self.player.capital > self.amount + 30:
            self.player.capital -= self.amount
            self.player.save()
            LogBook.objects.create(player = self.player, message = "%.2f Million paid as loan."%self.amount)
            if self.time_remaining <= 1:
                self.delete()
            else:
                self.time_remaining -= 1
                self.save()
        else:
            if self.time_remaining <= 1:
                self.mortaged_industries.all().delete()
                self.delete()
                LogBook.objects.create(player = self.player, message = "Industries taken over by government, due to non payment of loans.")
            else:
                self.amount *= self.time_remaining/(self.time_remaining-1)
                self.time_remaining = F('time_remaining') - 1
                self.player.loan_defaults = F('loan_defaults') + 1
                self.save()
                LogBook.objects.create(player = self.player, message = "Loan amount increased due to loan default")

def transport_check(self):
    if hasattr(self , 'transport') and not(self.transport == None):
        if self.state not in self.transport.states.all():
            raise ValidationError("Transport does not pass through state.")
        if self.transport.player != self.player:
            raise ValidationError("You cant use someone else's transport")

def check_player_research_level(self):
    if self.player.research_level < self.type.research_level:
        raise ValidationError("You are not qualified enough to build this Industry.")