# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Tx.price'
        db.delete_column(u'history_tx', 'price')

        # Adding field 'Tx.open'
        db.add_column(u'history_tx', 'open',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=0),
                      keep_default=False)

        # Adding field 'Tx.high'
        db.add_column(u'history_tx', 'high',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=0),
                      keep_default=False)

        # Adding field 'Tx.low'
        db.add_column(u'history_tx', 'low',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=0),
                      keep_default=False)

        # Adding field 'Tx.close'
        db.add_column(u'history_tx', 'close',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Tx.price'
        db.add_column(u'history_tx', 'price',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=12, decimal_places=0),
                      keep_default=False)

        # Deleting field 'Tx.open'
        db.delete_column(u'history_tx', 'open')

        # Deleting field 'Tx.high'
        db.delete_column(u'history_tx', 'high')

        # Deleting field 'Tx.low'
        db.delete_column(u'history_tx', 'low')

        # Deleting field 'Tx.close'
        db.delete_column(u'history_tx', 'close')


    models = {
        u'history.taiex': {
            'Meta': {'object_name': 'Taiex'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'history.tx': {
            'Meta': {'object_name': 'Tx'},
            'close': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '0'}),
            'high': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'low': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '0'}),
            'open': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '0'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['history']