# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'GlobalConstants.current_day'
        db.add_column(u'game_globalconstants', 'current_day',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'GlobalConstants.current_month'
        db.add_column(u'game_globalconstants', 'current_month',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'GlobalConstants.current_year'
        db.add_column(u'game_globalconstants', 'current_year',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1970),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'GlobalConstants.current_day'
        db.delete_column(u'game_globalconstants', 'current_day')

        # Deleting field 'GlobalConstants.current_month'
        db.delete_column(u'game_globalconstants', 'current_month')

        # Deleting field 'GlobalConstants.current_year'
        db.delete_column(u'game_globalconstants', 'current_year')


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
            'max_research_level': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'monthly_research_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'tax_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'vehicle_variable_limit': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        }
    }

    complete_apps = ['game']