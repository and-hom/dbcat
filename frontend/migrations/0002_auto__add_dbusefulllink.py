# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DbUsefullLink'
        db.create_table('frontend_dbusefulllink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['frontend.Db'])),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('frontend', ['DbUsefullLink'])


    def backwards(self, orm):
        # Deleting model 'DbUsefullLink'
        db.delete_table('frontend_dbusefulllink')


    models = {
        'frontend.booleanfilter': {
            'Meta': {'object_name': 'BooleanFilter', '_ormbases': ['frontend.Filter']},
            'filter_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['frontend.Filter']", 'unique': 'True', 'primary_key': 'True'})
        },
        'frontend.db': {
            'Meta': {'object_name': 'Db'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'short_description': ('django.db.models.fields.TextField', [], {'max_length': '512'})
        },
        'frontend.dbparam': {
            'Meta': {'object_name': 'DbParam'},
            'db': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['frontend.Db']"}),
            'filter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['frontend.Filter']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'frontend.dbusefulllink': {
            'Meta': {'object_name': 'DbUsefullLink'},
            'db': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['frontend.Db']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'frontend.filter': {
            'Meta': {'object_name': 'Filter'},
            'code': ('django.db.models.fields.CharField', [], {'primary_key': 'True', 'max_length': '32', 'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'frontend.intrangefilter': {
            'Meta': {'object_name': 'IntRangeFilter', '_ormbases': ['frontend.Filter']},
            'filter_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['frontend.Filter']", 'unique': 'True', 'primary_key': 'True'}),
            'max': ('django.db.models.fields.IntegerField', [], {}),
            'min': ('django.db.models.fields.IntegerField', [], {})
        },
        'frontend.selectdbparam': {
            'Meta': {'object_name': 'SelectDbParam', '_ormbases': ['frontend.DbParam']},
            'dbparam_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['frontend.DbParam']", 'unique': 'True', 'primary_key': 'True'})
        },
        'frontend.selectdbparamoption': {
            'Meta': {'object_name': 'SelectDbParamOption'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['frontend.SelectOption']"}),
            'param': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['frontend.SelectDbParam']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'frontend.selectfilter': {
            'Meta': {'object_name': 'SelectFilter', '_ormbases': ['frontend.Filter']},
            'filter_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['frontend.Filter']", 'unique': 'True', 'primary_key': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'frontend.selectoption': {
            'Meta': {'object_name': 'SelectOption'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'filter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['frontend.SelectFilter']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'frontend.simpledbparam': {
            'Meta': {'object_name': 'SimpleDbParam', '_ormbases': ['frontend.DbParam']},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '512'}),
            'dbparam_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['frontend.DbParam']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['frontend']