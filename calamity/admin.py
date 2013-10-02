from django.contrib import admin
from calamity.models import Calamity, CalamityOccurence

#admin module for calamity

class CalamityAdmin(admin.ModelAdmin):
    list_display = ['name', 'severity', 'probability_number']
    search_fields = ['states__name']

class CalamityOccurenceAdmin(admin.ModelAdmin):
    list_display = ['type', 'state', 'time_remaining']
    search_fields = ['state__name']

admin.site.register(Calamity,CalamityAdmin)
admin.site.register(CalamityOccurence,CalamityOccurenceAdmin)