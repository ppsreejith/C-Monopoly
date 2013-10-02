# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Player'
        db.create_table(u'player_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('monthly_carbon_total', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('net_worth', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=2)),
            ('capital', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=2)),
            ('research_level', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('brand', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=2)),
            ('extra_energy', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('energy_capacity', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('loan_defaults', self.gf('django.db.models.fields.IntegerField')()),
            ('suspended', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('shutdown', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user_login_id', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True)),
        ))
        db.send_create_signal(u'player', ['Player'])

        # Adding model 'ResearchProject'
        db.create_table(u'player_researchproject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['player.Player'])),
            ('time_remaining', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'player', ['ResearchProject'])


    def backwards(self, orm):
        # Deleting model 'Player'
        db.delete_table(u'player_player')

        # Deleting model 'ResearchProject'
        db.delete_table(u'player_researchproject')


    models = {
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
        u'player.researchproject': {
            'Meta': {'object_name': 'ResearchProject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['player.Player']"}),
            'time_remaining': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['player']