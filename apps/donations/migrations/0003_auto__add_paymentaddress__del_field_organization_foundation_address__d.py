# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PaymentAddress'
        db.create_table(u'donations_paymentaddress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_position', self.gf('django.db.models.fields.IntegerField')()),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payment_addresses', to=orm['donations.Organization'])),
            ('address', self.gf('apps.donations.fields.BitcoinAddressField')(max_length=34)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'donations', ['PaymentAddress'])

        # Deleting field 'Organization.foundation_address'
        db.delete_column(u'donations_organization', 'foundation_address')

        # Deleting field 'Organization.freicoin_address'
        db.delete_column(u'donations_organization', 'freicoin_address')

        # Deleting field 'Organization.bitcoin_address'
        db.delete_column(u'donations_organization', 'bitcoin_address')


    def backwards(self, orm):
        # Deleting model 'PaymentAddress'
        db.delete_table(u'donations_paymentaddress')

        # Adding field 'Organization.foundation_address'
        db.add_column(u'donations_organization', 'foundation_address',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=34, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Organization.freicoin_address'
        raise RuntimeError("Cannot reverse this migration. 'Organization.freicoin_address' and its values cannot be restored.")
        # Adding field 'Organization.bitcoin_address'
        db.add_column(u'donations_organization', 'bitcoin_address',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=34, blank=True),
                      keep_default=False)


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
        u'donations.organization': {
            'Meta': {'object_name': 'Organization'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.CharField', [], {'max_length': '1500'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '350'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'donations.paymentaddress': {
            'Meta': {'ordering': "['_position']", 'object_name': 'PaymentAddress'},
            '_position': ('django.db.models.fields.IntegerField', [], {}),
            'address': ('apps.donations.fields.BitcoinAddressField', [], {'max_length': '34'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payment_addresses'", 'to': u"orm['donations.Organization']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['donations']
