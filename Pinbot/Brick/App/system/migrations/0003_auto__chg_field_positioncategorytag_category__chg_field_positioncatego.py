# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'PositionCategoryTag.category'
        db.alter_column(u'system_positioncategorytag', 'category_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['system.PositionCategory']))

        # Changing field 'PositionCategoryTag.parent'
        db.alter_column(u'system_positioncategorytag', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, on_delete=models.SET_NULL, to=orm['system.PositionCategoryTag']))

    def backwards(self, orm):

        # Changing field 'PositionCategoryTag.category'
        db.alter_column(u'system_positioncategorytag', 'category_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['system.PositionCategory']))

        # Changing field 'PositionCategoryTag.parent'
        db.alter_column(u'system_positioncategorytag', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['system.PositionCategoryTag'], null=True))

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
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'category_tags'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['system.PositionCategory']"}),
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_tags'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['system.PositionCategoryTag']"})
        }
    }

    complete_apps = ['system']