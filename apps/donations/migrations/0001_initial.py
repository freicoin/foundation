# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Organization'
        db.create_table(u'donations_organization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('freicoin_address', self.gf('django.db.models.fields.CharField')(max_length=34)),
            ('bitcoin_address', self.gf('django.db.models.fields.CharField')(max_length=34, blank=True)),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=350)),
            ('long_description', self.gf('django.db.models.fields.CharField')(max_length=1500)),
            ('foundation_address', self.gf('django.db.models.fields.CharField')(max_length=34, blank=True)),
        ))
        db.send_create_signal(u'donations', ['Organization'])


    def backwards(self, orm):
        # Deleting model 'Organization'
        db.delete_table(u'donations_organization')


    models = {
        u'donations.organization': {
            'Meta': {'object_name': 'Organization'},
            'bitcoin_address': ('django.db.models.fields.CharField', [], {'max_length': '34', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'foundation_address': ('django.db.models.fields.CharField', [], {'max_length': '34', 'blank': 'True'}),
            'freicoin_address': ('django.db.models.fields.CharField', [], {'max_length': '34'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.CharField', [], {'max_length': '1500'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '350'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['donations']