# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'GlobalConstants.carbon_selling_price'
        db.delete_column(u'game_globalconstants', 'carbon_selling_price')


    def backwards(self, orm):
        # Adding field 'GlobalConstants.carbon_selling_price'
        db.add_column(u'game_globalconstants', 'carbon_selling_price',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=2),
                      keep_default=False)


    models = {
        u'game.globalconstants': {
            'Meta': {'object_name': 'GlobalConstants'},
            'carbon_buying_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'energy_buying_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'energy_selling_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_capital': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            'initial_research_time': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'loan_interest_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'max_research_level': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'monthly_research_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'tax_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'vehicle_variable_limit': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        }
    }

    complete_apps = ['game']