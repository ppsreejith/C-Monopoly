from django.contrib import admin
from industry.models import ProductIndustry, Factory, LoansCreated
from industry.forms import LoansCreatedForm

#Admin module for Industry

class FactoryAdmin(admin.ModelAdmin):
    list_display = ['type','state','player']
    search_fields = ['state__name','player__name']

class ProductIndustryAdmin(admin.ModelAdmin):
    list_display = ['name', 'initial_cost', 'unit']
    search_fields = ['name','states__name']

class LoansCreatedAdmin(admin.ModelAdmin):
    search_fields = ['player__name']
    form = LoansCreatedForm

admin.site.register(ProductIndustry,ProductIndustryAdmin)
admin.site.register(Factory,FactoryAdmin)
admin.site.register(LoansCreated, LoansCreatedAdmin)