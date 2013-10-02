# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Transport'
        db.create_table(u'transport_transport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('research_level', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('minimum_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('stopping_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('travel_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('max_stops', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('carbon_cost_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
        ))
        db.send_create_signal(u'transport', ['Transport'])

        # Adding M2M table for field states on 'Transport'
        m2m_table_name = db.shorten_name(u'transport_transport_states')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('transport', models.ForeignKey(orm[u'transport.transport'], null=False)),
            ('state', models.ForeignKey(orm[u'govt.state'], null=False))
        ))
        db.create_unique(m2m_table_name, ['transport_id', 'state_id'])

        # Adding model 'TransportCreated'
        db.create_table(u'transport_transportcreated', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('transport', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transport.Transport'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['player.Player'])),
        ))
        db.send_create_signal(u'transport', ['TransportCreated'])

        # Adding M2M table for field states on 'TransportCreated'
        m2m_table_name = db.shorten_name(u'transport_transportcreated_states')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('transportcreated', models.ForeignKey(orm[u'transport.transportcreated'], null=False)),
            ('state', models.ForeignKey(orm[u'govt.state'], null=False))
        ))
        db.create_unique(m2m_table_name, ['transportcreated_id', 'state_id'])


    def backwards(self, orm):
        # Deleting model 'Transport'
        db.delete_table(u'transport_transport')

        # Removing M2M table for field states on 'Transport'
        db.delete_table(db.shorten_name(u'transport_transport_states'))

        # Deleting model 'TransportCreated'
        db.delete_table(u'transport_transportcreated')

        # Removing M2M table for field states on 'TransportCreated'
        db.delete_table(db.shorten_name(u'transport_transportcreated_states'))


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

    complete_apps = ['transport']