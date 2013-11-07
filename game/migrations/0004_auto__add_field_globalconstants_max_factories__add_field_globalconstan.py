# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'GlobalConstants.max_factories'
        db.add_column(u'game_globalconstants', 'max_factories',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=20),
                      keep_default=False)

        # Adding field 'GlobalConstants.max_powerplants'
        db.add_column(u'game_globalconstants', 'max_powerplants',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=20),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'GlobalConstants.max_factories'
        db.delete_column(u'game_globalconstants', 'max_factories')

        # Deleting field 'GlobalConstants.max_powerplants'
        db.delete_column(u'game_globalconstants', 'max_powerplants')


    models = {
        u'game.globalconstants': {
            'Meta': {'object_name': 'GlobalConstants'},
            'carbon_buying_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'current_day': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'current_month': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'current_year': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1970'}),
            'energy_buying_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'energy_selling_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_capital': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            'initial_research_time': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'loan_interest_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'max_factories': ('django.db.models.fields.PositiveIntegerField', [], {'default': '20'}),
            'max_powerplants': ('django.db.models.fields.PositiveIntegerField', [], {'default': '20'}),
            'max_research_level': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'monthly_research_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'tax_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'vehicle_variable_limit': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        }
    }

    complete_apps = ['game']