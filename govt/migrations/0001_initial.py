# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'State'
        db.create_table(u'govt_state', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('coordx', self.gf('django.db.models.fields.IntegerField')()),
            ('coordy', self.gf('django.db.models.fields.IntegerField')()),
            ('population', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('research_level', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('capacity', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('energy_plant_capacity', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('income', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('growth_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=4)),
            ('income_growth_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=4)),
        ))
        db.send_create_signal(u'govt', ['State'])

        # Adding unique constraint on 'State', fields ['coordx', 'coordy']
        db.create_unique(u'govt_state', ['coordx', 'coordy'])

        # Adding model 'LoansCreated'
        db.create_table(u'govt_loanscreated', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.OneToOneField')(related_name='Loan', unique=True, to=orm['player.Player'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('time_remaining', self.gf('django.db.models.fields.PositiveIntegerField')()),
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

        # Adding model 'AquireRecord'
        db.create_table(u'govt_aquirerecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('to_player', self.gf('django.db.models.fields.related.OneToOneField')(related_name='Offer', unique=True, to=orm['player.Player'])),
            ('from_player', self.gf('django.db.models.fields.related.OneToOneField')(related_name='Acquisition', unique=True, to=orm['player.Player'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=5)),
        ))
        db.send_create_signal(u'govt', ['AquireRecord'])

        # Adding model 'EnergyDeal'
        db.create_table(u'govt_energydeal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='EnergyOffer', to=orm['player.Player'])),
            ('to_player', self.gf('django.db.models.fields.related.OneToOneField')(related_name='EnergyContract', unique=True, to=orm['player.Player'])),
            ('amount_energy', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=5)),
        ))
        db.send_create_signal(u'govt', ['EnergyDeal'])


    def backwards(self, orm):
        # Removing unique constraint on 'State', fields ['coordx', 'coordy']
        db.delete_unique(u'govt_state', ['coordx', 'coordy'])

        # Deleting model 'State'
        db.delete_table(u'govt_state')

        # Deleting model 'LoansCreated'
        db.delete_table(u'govt_loanscreated')

        # Removing M2M table for field mortaged_industries on 'LoansCreated'
        db.delete_table(db.shorten_name(u'govt_loanscreated_mortaged_industries'))

        # Deleting model 'AquireRecord'
        db.delete_table(u'govt_aquirerecord')

        # Deleting model 'EnergyDeal'
        db.delete_table(u'govt_energydeal')


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
        u'govt.loanscreated': {
            'Meta': {'object_name': 'LoansCreated'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mortaged_industries': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['industry.Factory']", 'symmetrical': 'False'}),
            'player': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'Loan'", 'unique': 'True', 'to': u"orm['player.Player']"}),
            'time_remaining': ('django.db.models.fields.PositiveIntegerField', [], {})
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
        u'industry.factory': {
            'Meta': {'object_name': 'Factory'},
            'actual_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['player.Player']"}),
            'products_last_month': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'selling_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '5'}),
            'shut_down': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['govt.State']"}),
            'transport': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transport.TransportCreated']", 'null': 'True', 'blank': 'True'}),
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
            'maintenance_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'maintenance_energy': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'research_level': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'states': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['govt.State']", 'symmetrical': 'False'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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
            'netWorth': ('django.db.models.fields.DecimalField', [], {'default': '100', 'max_digits': '15', 'decimal_places': '2'}),
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

    complete_apps = ['govt']