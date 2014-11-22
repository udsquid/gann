# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Strategy', fields ['name']
        db.create_unique(u'order_strategy', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Strategy', fields ['name']
        db.delete_unique(u'order_strategy', ['name'])


    models = {
        u'order.strategy': {
            'Meta': {'object_name': 'Strategy'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '8'})
        }
    }

    complete_apps = ['order']