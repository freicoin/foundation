# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'AvailableAddress'
        db.delete_table(u'donations_availableaddress')

        # Deleting field 'Organization.foundation_address'
        db.delete_column(u'donations_organization', 'foundation_address_id')

        # Adding field 'Organization.created'
        db.add_column(u'donations_organization', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 9, 16, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Organization.validated'
        db.add_column(u'donations_organization', 'validated',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)


        # Changing field 'Organization.category'
        db.alter_column(u'donations_organization', 'category_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['donations.Category']))

    def backwards(self, orm):
        # Adding model 'AvailableAddress'
        db.create_table(u'donations_availableaddress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('apps.donations.fields.BitcoinAddressField')(max_length=34)),
        ))
        db.send_create_signal(u'donations', ['AvailableAddress'])

        # Adding field 'Organization.foundation_address'
        db.add_column(u'donations_organization', 'foundation_address',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='foundation_address_for', null=True, to=orm['donations.PaymentAddress']),
                      keep_default=False)

        # Deleting field 'Organization.created'
        db.delete_column(u'donations_organization', 'created')

        # Deleting field 'Organization.validated'
        db.delete_column(u'donations_organization', 'validated')


        # Changing field 'Organization.category'
        db.alter_column(u'donations_organization', 'category_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['donations.Category']))

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
        u'donations.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_categories'", 'null': 'True', 'to': u"orm['donations.Category']"})
        },
        u'donations.organization': {
            'Meta': {'object_name': 'Organization'},
            'bitcoin_address': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bitcoin_address_for'", 'null': 'True', 'to': u"orm['donations.PaymentAddress']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'organizations'", 'to': u"orm['donations.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'freicoin_address': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'freicoin_address_for'", 'null': 'True', 'to': u"orm['donations.PaymentAddress']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '350'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'validated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'validated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'organizations_validated'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'donations.paymentaddress': {
            'Meta': {'object_name': 'PaymentAddress'},
            'address': ('apps.donations.fields.BitcoinAddressField', [], {'max_length': '34'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payment_addresses'", 'to': u"orm['donations.Organization']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['donations']