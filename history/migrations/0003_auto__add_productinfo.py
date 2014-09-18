# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProductInfo'
        db.create_table(u'history_productinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('market', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('tick_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=5)),
        ))
        db.send_create_signal(u'history', ['ProductInfo'])


    def backwards(self, orm):
        # Deleting model 'ProductInfo'
        db.delete_table(u'history_productinfo')


    models = {
        u'history.productinfo': {
            'Meta': {'object_name': 'ProductInfo'},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'tick_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '5'})
        },
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