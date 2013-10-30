# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Calamity'
        db.create_table(u'calamity_calamity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('severity', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('probability_number', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'calamity', ['Calamity'])

        # Adding M2M table for field states on 'Calamity'
        m2m_table_name = db.shorten_name(u'calamity_calamity_states')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('calamity', models.ForeignKey(orm[u'calamity.calamity'], null=False)),
            ('state', models.ForeignKey(orm[u'govt.state'], null=False))
        ))
        db.create_unique(m2m_table_name, ['calamity_id', 'state_id'])

        # Adding model 'CalamityOccurence'
        db.create_table(u'calamity_calamityoccurence', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['calamity.Calamity'])),
            ('state', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['govt.State'], unique=True)),
            ('time_remaining', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'calamity', ['CalamityOccurence'])


    def backwards(self, orm):
        # Deleting model 'Calamity'
        db.delete_table(u'calamity_calamity')

        # Removing M2M table for field states on 'Calamity'
        db.delete_table(db.shorten_name(u'calamity_calamity_states'))

        # Deleting model 'CalamityOccurence'
        db.delete_table(u'calamity_calamityoccurence')


    models = {
        u'calamity.calamity': {
            'Meta': {'object_name': 'Calamity'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'probability_number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'severity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'states': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['govt.State']", 'symmetrical': 'False'})
        },
        u'calamity.calamityoccurence': {
            'Meta': {'object_name': 'CalamityOccurence'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['govt.State']", 'unique': 'True'}),
            'time_remaining': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['calamity.Calamity']"})
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
        }
    }

    complete_apps = ['calamity']