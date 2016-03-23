# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CompanyWelfare'
        db.create_table(u'system_companywelfare', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('code_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('sort', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
        ))
        db.send_create_signal(u'system', ['CompanyWelfare'])

        # Adding model 'CompanyCategoryPrefer'
        db.create_table(u'system_companycategoryprefer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('code_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('sort', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
        ))
        db.send_create_signal(u'system', ['CompanyCategoryPrefer'])


    def backwards(self, orm):
        # Deleting model 'CompanyWelfare'
        db.delete_table(u'system_companywelfare')

        # Deleting model 'CompanyCategoryPrefer'
        db.delete_table(u'system_companycategoryprefer')


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
        u'system.companycategoryprefer': {
            'Meta': {'object_name': 'CompanyCategoryPrefer'},
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'})
        },
        u'system.companywelfare': {
            'Meta': {'object_name': 'CompanyWelfare'},
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'})
        },
        u'system.positioncategory': {
            'Meta': {'object_name': 'PositionCategory'},
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'system.positioncategorytag': {
            'Meta': {'object_name': 'PositionCategoryTag'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'category_tags'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['system.PositionCategory']"}),
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_tags'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['system.PositionCategoryTag']"})
        }
    }

    complete_apps = ['system']