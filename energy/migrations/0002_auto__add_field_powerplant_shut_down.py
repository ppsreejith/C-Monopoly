# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PowerPlant.shut_down'
        db.add_column(u'energy_powerplant', 'shut_down',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PowerPlant.shut_down'
        db.delete_column(u'energy_powerplant', 'shut_down')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'energy.energyindustry': {
            'Meta': {'object_name': 'EnergyIndustry'},
            'annual_value_decrease': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'carbon_per_unit': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'maintenance_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'output': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'research_level': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'states': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['govt.State']", 'symmetrical': 'False'})
        },
        u'energy.powerplant': {
            'Meta': {'object_name': 'PowerPlant'},
            'actual_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['player.Player']"}),
            'shut_down': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['govt.State']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['energy.EnergyIndustry']"})
        },
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
        u'player.player': {
            'Meta': {'object_name': 'Player'},
            'brand': ('django.db.models.fields.DecimalField', [], {'default': '5', 'max_digits': '4', 'decimal_places': '2'}),
            'capital': ('django.db.models.fields.DecimalField', [], {'default': "'100.00'", 'max_digits': '15', 'decimal_places': '2'}),
            'energy_capacity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '30'}),
            'extra_energy': ('django.db.models.fields.PositiveIntegerField', [], {'default': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_month_total': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'loan_defaults': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'monthly_carbon_total': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'netWorth': ('django.db.models.fields.DecimalField', [], {'default': "'100.00'", 'max_digits': '15', 'decimal_places': '2'}),
            'research_level': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'selling_energy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'suspended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'user_login_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['energy']