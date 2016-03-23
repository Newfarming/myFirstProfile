# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'City'
        db.create_table(u'system_city', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'system', ['City'])

        # Adding model 'CompanyCategory'
        db.create_table(u'system_companycategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('code_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'system', ['CompanyCategory'])

        # Adding model 'PositionCategory'
        db.create_table(u'system_positioncategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('code_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'system', ['PositionCategory'])

        # Adding model 'PositionCategoryTag'
        db.create_table(u'system_positioncategorytag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('code_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['system.PositionCategory'])),
        ))
        db.send_create_signal(u'system', ['PositionCategoryTag'])


    def backwards(self, orm):
        # Deleting model 'City'
        db.delete_table(u'system_city')

        # Deleting model 'CompanyCategory'
        db.delete_table(u'system_companycategory')

        # Deleting model 'PositionCategory'
        db.delete_table(u'system_positioncategory')

        # Deleting model 'PositionCategoryTag'
        db.delete_table(u'system_positioncategorytag')


    models = {
        u'system.city': {
            'Meta': {'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'system.companycategory': {
            'Meta': {'object_name': 'CompanyCategory'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'system.positioncategory': {
            'Meta': {'object_name': 'PositionCategory'},
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'system.positioncategorytag': {
            'Meta': {'object_name': 'PositionCategoryTag'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['system.PositionCategory']"}),
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['system']