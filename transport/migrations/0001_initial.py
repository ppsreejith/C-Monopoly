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
            ('initial_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('stopping_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('travel_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('max_stops', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('carbon_cost_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('energy_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
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
            'capital': ('django.db.models.fields.DecimalField', [], {'default': '100', 'max_digits': '15', 'decimal_places': '2'}),
            'energy_capacity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '30'}),
            'extra_energy': ('django.db.models.fields.PositiveIntegerField', [], {'default': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_month_total': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'loan_defaults': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'monthly_carbon_total': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'net_worth': ('django.db.models.fields.DecimalField', [], {'default': '100', 'max_digits': '15', 'decimal_places': '2'}),
            'research_level': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'shutdown': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'suspended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'user_login_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'transport.transport': {
            'Meta': {'object_name': 'Transport'},
            'carbon_cost_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'energy_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'max_stops': ('django.db.models.fields.PositiveIntegerField', [], {}),
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