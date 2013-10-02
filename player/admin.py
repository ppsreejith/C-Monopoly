from django.contrib import admin
from player.models import Player, ResearchProject

#Admin module for Player

class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name','net_worth','capital', 'suspended','shutdown']
    list_editable = ['net_worth','capital', 'suspended']
    search_fields = ['name']

admin.site.register(Player, PlayerAdmin)
admin.site.register(ResearchProject)