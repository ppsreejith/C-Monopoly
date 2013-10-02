from django.contrib import admin
from energy.models import EnergyIndustry, PowerPlant

#admin module for energy

class PowerPlantAdmin(admin.ModelAdmin):
    list_display = ['type','state','player']
    search_fields = ['state__name','player__name']

class EnergyIndustryAdmin(admin.ModelAdmin):
    list_display = ['name', 'initial_cost','output']
    search_fields = ['states__name','name']

admin.site.register(EnergyIndustry,EnergyIndustryAdmin)
admin.site.register(PowerPlant,PowerPlantAdmin)