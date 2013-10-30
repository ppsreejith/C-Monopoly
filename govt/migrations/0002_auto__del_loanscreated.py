# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'LoansCreated'
        db.delete_table(u'govt_loanscreated')

        # Removing M2M table for field mortaged_industries on 'LoansCreated'
        db.delete_table(db.shorten_name(u'govt_loanscreated_mortaged_industries'))


    def backwards(self, orm):
        # Adding model 'LoansCreated'
        db.create_table(u'govt_loanscreated', (
            ('player', self.gf('django.db.models.fields.related.OneToOneField')(related_name='Loan', unique=True, to=orm['player.Player'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('time_remaining', self.gf('django.db.models.fields.PositiveIntegerField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'govt', ['LoansCreated'])

        # Adding M2M table for field mortaged_industries on 'LoansCreated'
        m2m_table_name = db.shorten_name(u'govt_loanscreated_mortaged_industries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('loanscreated', models.ForeignKey(orm[u'govt.loanscreated'], null=False)),
            ('factory', models.ForeignKey(orm[u'industry.factory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['loanscreated_id', 'factory_id'])


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
        u'govt.aquirerecord': {
            'Meta': {'object_name': 'AquireRecord'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '5'}),
            'from_player': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'Acquisition'", 'unique': 'True', 'to': u"orm['player.Player']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_player': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'Offer'", 'unique': 'True', 'to': u"orm['player.Player']"})
        },
        u'govt.energydeal': {
            'Meta': {'object_name': 'EnergyDeal'},
            'amount_energy': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '5'}),
            'from_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'EnergyOffer'", 'to': u"orm['player.Player']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_player': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'EnergyContract'", 'unique': 'True', 'to': u"orm['player.Player']"})
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
            'net_worth': ('django.db.models.fields.DecimalField', [], {'default': "'100.00'", 'max_digits': '15', 'decimal_places': '2'}),
            'research_level': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'selling_energy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'suspended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'user_login_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['govt']