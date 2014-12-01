# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Order'
        db.create_table(u'order_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('strategy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['order.Strategy'])),
            ('open_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('open_price', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('size', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('close_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('close_price', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=8)),
        ))
        db.send_create_signal(u'order', ['Order'])


    def backwards(self, orm):
        # Deleting model 'Order'
        db.delete_table(u'order_order')


    models = {
        u'order.order': {
            'Meta': {'object_name': 'Order'},
            'close_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'close_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'open_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'open_time': ('django.db.models.fields.DateTimeField', [], {}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'strategy': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['order.Strategy']"})
        },
        u'order.strategy': {
            'Meta': {'object_name': 'Strategy'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '8'})
        }
    }

    complete_apps = ['order']