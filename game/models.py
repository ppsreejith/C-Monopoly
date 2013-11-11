from django.db.models import F
from django.db import models
from django.core.exceptions import ValidationError

#Only one should be instantiated
class GlobalConstants(models.Model):
    carbon_buying_price = models.DecimalField(max_digits = 9, decimal_places = 2, help_text = "price of carbon. (In thousands)" ) #price of carbon credits.
    energy_buying_price = models.DecimalField(max_digits = 9, decimal_places = 2, help_text = "price at which govt buys energy") #price at which energy sold to govt.
    energy_selling_price = models.DecimalField(max_digits = 9, decimal_places = 2, help_text = "price at which govt sells energy") #price at which govt sells energy
    tax_rate = models.DecimalField(max_digits = 5, decimal_places = 2, help_text="Percentage of revenue as tax.") #revenue tax
    loan_interest_rate = models.DecimalField(max_digits = 5, decimal_places = 2, help_text="Percentage of loan as interest") #Loan Interest Rate
    vehicle_variable_limit = models.DecimalField(max_digits = 5, decimal_places = 2, help_text="Maximum deviation in percentage.") #Variable Vehicle Cost Limit.
    max_research_level = models.PositiveIntegerField(help_text="Maximum Research Level (Integer)") #Maximum Research Level
    initial_research_time = models.PositiveIntegerField(help_text = "In number of months (Integer)") # will be multiplied by research level
    monthly_research_cost = models.DecimalField(max_digits = 9, decimal_places = 2, help_text = "In cost per month, in millions") # will be multiplied by research level
    initial_capital = models.DecimalField(max_digits = 15, decimal_places = 2, help_text = "In millions")
    current_day = models.PositiveIntegerField(default = 1)
    current_month = models.PositiveIntegerField(default = 1)
    current_year = models.PositiveIntegerField(default = 1970)
    max_factories = models.PositiveIntegerField(default = 20)
    max_powerplants = models.PositiveIntegerField(default = 20)
    def __unicode__(self):
        return "Global Constants"
    #Only one global constants instance necessary
    def clean(self):
        validate_only_one_instance(self)
    class Meta:
        verbose_name = verbose_name_plural = "Global Constants"
    
    def nextDay(self):
        if self.current_day >= 30 and self.current_month in [4,6,9,11]:
            self.current_day = 1
            self.current_month = F('current_month') + 1
        elif self.current_day >= 31 and self.current_month in [1,3,5,7,8,10,12]:
            self.current_day = 1
            if self.current_month == 12:
                self.current_year = F('current_year') + 1
                self.current_month = 1
            else:
                self.current_month = F('current_month') + 1
        elif self.current_day >= 28 and self.current_month == 2:
            self.current_day = 1
            self.current_month = 3
        elif self.current_month > 12:
            self.current_month = 1
        else:
            self.current_day = F('current_day') + 1
        self.save()

#Check if only one instance
def validate_only_one_instance(obj):
    model = obj.__class__
    if model.objects.count() > 0 and  obj.id != model.objects.get().id:
        raise ValidationError("Can only create 1 %s instance" % model.__name__)