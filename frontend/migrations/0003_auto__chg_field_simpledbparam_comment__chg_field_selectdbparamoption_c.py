# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'SimpleDbParam.comment'
        db.alter_column('frontend_simpledbparam', 'comment', self.gf('django.db.models.fields.TextField')(max_length=512, null=True))

        # Changing field 'SelectDbParamOption.comment'
        db.alter_column('frontend_selectdbparamoption', 'comment', self.gf('django.db.models.fields.TextField')(max_length=512, null=True))

    def backwards(self, orm):

        # Changing field 'SimpleDbParam.comment'
        db.alter_column('frontend_simpledbparam', 'comment', self.gf('django.db.models.fields.TextField')(max_length=512, default=' '))

        # Changing field 'SelectDbParamOption.comment'
        db.alter_column('frontend_selectdbparamoption', 'comment', self.gf('django.db.models.fields.TextField')(max_length=512, default=' '))

    models = {
        'frontend.booleanfilter': {
            'Meta': {'_ormbases': ['frontend.Filter'], 'object_name': 'BooleanFilter'},
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
            'code': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True', 'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'frontend.intrangefilter': {
            'Meta': {'_ormbases': ['frontend.Filter'], 'object_name': 'IntRangeFilter'},
            'filter_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['frontend.Filter']", 'unique': 'True', 'primary_key': 'True'}),
            'max': ('django.db.models.fields.IntegerField', [], {}),
            'min': ('django.db.models.fields.IntegerField', [], {})
        },
        'frontend.selectdbparam': {
            'Meta': {'_ormbases': ['frontend.DbParam'], 'object_name': 'SelectDbParam'},
            'dbparam_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['frontend.DbParam']", 'unique': 'True', 'primary_key': 'True'})
        },
        'frontend.selectdbparamoption': {
            'Meta': {'object_name': 'SelectDbParamOption'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['frontend.SelectOption']"}),
            'param': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['frontend.SelectDbParam']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'frontend.selectfilter': {
            'Meta': {'_ormbases': ['frontend.Filter'], 'object_name': 'SelectFilter'},
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
            'Meta': {'_ormbases': ['frontend.DbParam'], 'object_name': 'SimpleDbParam'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'dbparam_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['frontend.DbParam']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['frontend']