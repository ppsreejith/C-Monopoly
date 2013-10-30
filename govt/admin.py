from django.contrib import admin
from govt.models import State, AquireRecord, EnergyDeal

class StateAdmin(admin.ModelAdmin):
    list_editable = ['capacity', 'energy_plant_capacity',]
    search_fields = ['name']
    list_display = ['name', 'capacity','energy_plant_capacity',]    

admin.site.register(State, StateAdmin)
admin.site.register(AquireRecord)
admin.site.register(EnergyDeal)