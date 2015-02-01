# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Filter'
        db.create_table('frontend_filter', (
            ('code', self.gf('django.db.models.fields.CharField')(primary_key=True, max_length=32, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True, null=True)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=10)),
        ))
        db.send_create_signal('frontend', ['Filter'])

        # Adding model 'IntRangeFilter'
        db.create_table('frontend_intrangefilter', (
            ('filter_ptr', self.gf('django.db.models.fields.related.OneToOneField')(primary_key=True, unique=True, to=orm['frontend.Filter'])),
            ('min', self.gf('django.db.models.fields.IntegerField')()),
            ('max', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('frontend', ['IntRangeFilter'])

        # Adding model 'BooleanFilter'
        db.create_table('frontend_booleanfilter', (
            ('filter_ptr', self.gf('django.db.models.fields.related.OneToOneField')(primary_key=True, unique=True, to=orm['frontend.Filter'])),
        ))
        db.send_create_signal('frontend', ['BooleanFilter'])

        # Adding model 'SelectFilter'
        db.create_table('frontend_selectfilter', (
            ('filter_ptr', self.gf('django.db.models.fields.related.OneToOneField')(primary_key=True, unique=True, to=orm['frontend.Filter'])),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('frontend', ['SelectFilter'])

        # Adding model 'SelectOption'
        db.create_table('frontend_selectoption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['frontend.SelectFilter'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('frontend', ['SelectOption'])

        # Adding model 'Db'
        db.create_table('frontend_db', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('short_description', self.gf('django.db.models.fields.TextField')(max_length=512)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('homepage', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('frontend', ['Db'])

        # Adding model 'DbParam'
        db.create_table('frontend_dbparam', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('db', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['frontend.Db'])),
            ('filter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['frontend.Filter'])),
        ))
        db.send_create_signal('frontend', ['DbParam'])

        # Adding model 'SimpleDbParam'
        db.create_table('frontend_simpledbparam', (
            ('dbparam_ptr', self.gf('django.db.models.fields.related.OneToOneField')(primary_key=True, unique=True, to=orm['frontend.DbParam'])),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=512)),
        ))
        db.send_create_signal('frontend', ['SimpleDbParam'])

        # Adding model 'SelectDbParam'
        db.create_table('frontend_selectdbparam', (
            ('dbparam_ptr', self.gf('django.db.models.fields.related.OneToOneField')(primary_key=True, unique=True, to=orm['frontend.DbParam'])),
        ))
        db.send_create_signal('frontend', ['SelectDbParam'])

        # Adding model 'SelectDbParamOption'
        db.create_table('frontend_selectdbparamoption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('param', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['frontend.SelectDbParam'])),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['frontend.SelectOption'])),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=512)),
        ))
        db.send_create_signal('frontend', ['SelectDbParamOption'])


    def backwards(self, orm):
        # Deleting model 'Filter'
        db.delete_table('frontend_filter')

        # Deleting model 'IntRangeFilter'
        db.delete_table('frontend_intrangefilter')

        # Deleting model 'BooleanFilter'
        db.delete_table('frontend_booleanfilter')

        # Deleting model 'SelectFilter'
        db.delete_table('frontend_selectfilter')

        # Deleting model 'SelectOption'
        db.delete_table('frontend_selectoption')

        # Deleting model 'Db'
        db.delete_table('frontend_db')

        # Deleting model 'DbParam'
        db.delete_table('frontend_dbparam')

        # Deleting model 'SimpleDbParam'
        db.delete_table('frontend_simpledbparam')

        # Deleting model 'SelectDbParam'
        db.delete_table('frontend_selectdbparam')

        # Deleting model 'SelectDbParamOption'
        db.delete_table('frontend_selectdbparamoption')


    models = {
        'frontend.booleanfilter': {
            'Meta': {'_ormbases': ['frontend.Filter'], 'object_name': 'BooleanFilter'},
            'filter_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['frontend.Filter']"})
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
        'frontend.filter': {
            'Meta': {'object_name': 'Filter'},
            'code': ('django.db.models.fields.CharField', [], {'primary_key': 'True', 'max_length': '32', 'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'frontend.intrangefilter': {
            'Meta': {'_ormbases': ['frontend.Filter'], 'object_name': 'IntRangeFilter'},
            'filter_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['frontend.Filter']"}),
            'max': ('django.db.models.fields.IntegerField', [], {}),
            'min': ('django.db.models.fields.IntegerField', [], {})
        },
        'frontend.selectdbparam': {
            'Meta': {'_ormbases': ['frontend.DbParam'], 'object_name': 'SelectDbParam'},
            'dbparam_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['frontend.DbParam']"})
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
            'Meta': {'_ormbases': ['frontend.Filter'], 'object_name': 'SelectFilter'},
            'filter_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['frontend.Filter']"}),
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
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '512'}),
            'dbparam_ptr': ('django.db.models.fields.related.OneToOneField', [], {'primary_key': 'True', 'unique': 'True', 'to': "orm['frontend.DbParam']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['frontend']