# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Taiex'
        db.create_table(u'history_taiex', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
        ))
        db.send_create_signal(u'history', ['Taiex'])

        # Adding model 'Tx'
        db.create_table(u'history_tx', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=0)),
        ))
        db.send_create_signal(u'history', ['Tx'])


    def backwards(self, orm):
        # Deleting model 'Taiex'
        db.delete_table(u'history_taiex')

        # Deleting model 'Tx'
        db.delete_table(u'history_tx')


    models = {
        u'history.taiex': {
            'Meta': {'object_name': 'Taiex'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'history.tx': {
            'Meta': {'object_name': 'Tx'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '0'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['history']