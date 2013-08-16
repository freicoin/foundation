# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FaucetSend'
        db.create_table(u'faucet_faucetsend', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip_address', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('frc_address', self.gf('django.db.models.fields.CharField')(max_length=34)),
            ('tx_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'faucet', ['FaucetSend'])


    def backwards(self, orm):
        # Deleting model 'FaucetSend'
        db.delete_table(u'faucet_faucetsend')


    models = {
        u'faucet.faucetsend': {
            'Meta': {'object_name': 'FaucetSend'},
            'frc_address': ('django.db.models.fields.CharField', [], {'max_length': '34'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tx_id': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['faucet']