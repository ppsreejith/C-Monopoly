from django.contrib import admin
from transport.models import Transport, TransportCreated
from transport.forms import TransportForm, TransportCreatedForm

#Admin module for Transport

class TransportAdmin(admin.ModelAdmin):
    list_display = ['name','minimum_cost','travel_rate']
    search_fields = ['name','states__name']
    form = TransportForm

class TransportCreatedAdmin(admin.ModelAdmin):
    list_display = ['transport','player']
    search_fields = ['player__name','stops__name']
    form = TransportCreatedForm

admin.site.register(Transport, TransportAdmin)
admin.site.register(TransportCreated, TransportCreatedAdmin)