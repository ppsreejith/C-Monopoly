from django.contrib import admin
from player.models import Player, ResearchProject

#Admin module for Player

class PlayerAdmin(admin.ModelAdmin):
    list_display = ['user','netWorth','capital', 'suspended']
    list_editable = ['netWorth','capital', 'suspended']
    list_display_links = []

admin.site.register(Player, PlayerAdmin)
admin.site.register(ResearchProject)