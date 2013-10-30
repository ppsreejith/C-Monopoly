# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GlobalConstants'
        db.create_table(u'game_globalconstants', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('carbon_buying_price', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('carbon_selling_price', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('energy_buying_price', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('energy_selling_price', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('tax_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('loan_interest_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('vehicle_variable_limit', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('max_research_level', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('initial_research_time', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('monthly_research_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('initial_capital', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=2)),
        ))
        db.send_create_signal(u'game', ['GlobalConstants'])


    def backwards(self, orm):
        # Deleting model 'GlobalConstants'
        db.delete_table(u'game_globalconstants')


    models = {
        u'game.globalconstants': {
            'Meta': {'object_name': 'GlobalConstants'},
            'carbon_buying_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'carbon_selling_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
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