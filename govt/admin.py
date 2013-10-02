from django.contrib import admin
from govt.models import State, LoansCreated, AquireRecord, EnergyDeal, GlobalConstants
from govt.forms import LoansCreatedForm

#The admin module

class StateAdmin(admin.ModelAdmin):
    list_editable = ['capacity', 'energy_plant_capacity',]
    search_fields = ['name']
    list_display = ['name', 'capacity','energy_plant_capacity',]    

class LoansCreatedAdmin(admin.ModelAdmin):
    search_fields = ['player__name']
    form = LoansCreatedForm

admin.site.register(State, StateAdmin)
admin.site.register(LoansCreated, LoansCreatedAdmin)
admin.site.register(AquireRecord)
admin.site.register(EnergyDeal)
admin.site.register(GlobalConstants)