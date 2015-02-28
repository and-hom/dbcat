# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SelectFilter.multichoice'
        db.add_column('frontend_selectfilter', 'multichoice',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SelectFilter.multichoice'
        db.delete_column('frontend_selectfilter', 'multichoice')


    models = {
        'frontend.booleanfilter': {
            'Meta': {'object_name': 'BooleanFilter', '_ormbases': ['frontend.Filter']},
            'filter_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['frontend.Filter']", 'primary_key': 'True'})
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
            'code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'primary_key': 'True', 'max_length': '32'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'frontend.intrangefilter': {
            'Meta': {'object_name': 'IntRangeFilter', '_ormbases': ['frontend.Filter']},
            'filter_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['frontend.Filter']", 'primary_key': 'True'}),
            'max': ('django.db.models.fields.IntegerField', [], {}),
            'min': ('django.db.models.fields.IntegerField', [], {})
        },
        'frontend.selectdbparam': {
            'Meta': {'object_name': 'SelectDbParam', '_ormbases': ['frontend.DbParam']},
            'dbparam_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['frontend.DbParam']", 'primary_key': 'True'})
        },
        'frontend.selectdbparamoption': {
            'Meta': {'object_name': 'SelectDbParamOption'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True', 'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['frontend.SelectOption']"}),
            'param': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['frontend.SelectDbParam']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'frontend.selectfilter': {
            'Meta': {'object_name': 'SelectFilter', '_ormbases': ['frontend.Filter']},
            'filter_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['frontend.Filter']", 'primary_key': 'True'}),
            'multichoice': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'frontend.selectoption': {
            'Meta': {'object_name': 'SelectOption'},
            'code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32'}),
            'filter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['frontend.SelectFilter']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'frontend.simpledbparam': {
            'Meta': {'object_name': 'SimpleDbParam', '_ormbases': ['frontend.DbParam']},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True', 'max_length': '512'}),
            'dbparam_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['frontend.DbParam']", 'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['frontend']