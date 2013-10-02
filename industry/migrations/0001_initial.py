# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProductIndustry'
        db.create_table(u'industry_productindustry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('carbon_per_unit', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=5)),
            ('initial_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('maintenance_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('research_level', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('annual_value_decrease', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('cost_price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=5)),
            ('initial_energy', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('maintenance_energy', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('energy_per_unit', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=5)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'industry', ['ProductIndustry'])

        # Adding M2M table for field states on 'ProductIndustry'
        m2m_table_name = db.shorten_name(u'industry_productindustry_states')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('productindustry', models.ForeignKey(orm[u'industry.productindustry'], null=False)),
            ('state', models.ForeignKey(orm[u'govt.state'], null=False))
        ))
        db.create_unique(m2m_table_name, ['productindustry_id', 'state_id'])

        # Adding model 'Factory'
        db.create_table(u'industry_factory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['industry.ProductIndustry'])),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['govt.State'])),
            ('transport', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transport.TransportCreated'], null=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['player.Player'])),
            ('selling_price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=5)),
            ('actual_value', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('products_last_month', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('shut_down', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'industry', ['Factory'])


    def backwards(self, orm):
        # Deleting model 'ProductIndustry'
        db.delete_table(u'industry_productindustry')

        # Removing M2M table for field states on 'ProductIndustry'
        db.delete_table(db.shorten_name(u'industry_productindustry_states'))

        # Deleting model 'Factory'
        db.delete_table(u'industry_factory')


    models = {
        u'govt.state': {
            'Meta': {'unique_together': "(('coordx', 'coordy'),)", 'object_name': 'State'},
            'capacity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'coordx': ('django.db.models.fields.IntegerField', [], {}),
            'coordy': ('django.db.models.fields.IntegerField', [], {}),
            'energy_plant_capacity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'growth_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'income': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'income_growth_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'population': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'research_level': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'industry.factory': {
            'Meta': {'object_name': 'Factory'},
            'actual_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['player.Player']"}),
            'products_last_month': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'selling_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '5'}),
            'shut_down': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['govt.State']"}),
            'transport': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transport.TransportCreated']", 'null': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['industry.ProductIndustry']"})
        },
        u'industry.productindustry': {
            'Meta': {'object_name': 'ProductIndustry'},
            'annual_value_decrease': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'carbon_per_unit': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '5'}),
            'cost_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '5'}),
            'energy_per_unit': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'initial_energy': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'maintenance_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'maintenance_energy': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'research_level': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'states': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['govt.State']", 'symmetrical': 'False'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'player.player': {
            'Meta': {'object_name': 'Player'},
            'brand': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'}),
            'capital': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            'energy_capacity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'extra_energy': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loan_defaults': ('django.db.models.fields.IntegerField', [], {}),
            'monthly_carbon_total': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'net_worth': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            'research_level': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'shutdown': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'suspended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_login_id': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'})
        },
        u'transport.transport': {
            'Meta': {'object_name': 'Transport'},
            'carbon_cost_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_stops': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'minimum_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'research_level': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'states': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['govt.State']", 'symmetrical': 'False'}),
            'stopping_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'travel_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'})
        },
        u'transport.transportcreated': {
            'Meta': {'object_name': 'TransportCreated'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['player.Player']"}),
            'states': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['govt.State']", 'symmetrical': 'False'}),
            'transport': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transport.Transport']"})
        }
    }

    complete_apps = ['industry']