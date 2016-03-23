# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MailTemplateCategory'
        db.create_table(u'sendemail_mailtemplatecategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'sendemail', ['MailTemplateCategory'])

        # Adding model 'MailTemplate'
        db.create_table(u'sendemail_mailtemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sendemail.MailTemplateCategory'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('tag_id', self.gf('django.db.models.fields.IntegerField')(unique=True, null=True, blank=True)),
            ('tag_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'sendemail', ['MailTemplate'])


    def backwards(self, orm):
        # Deleting model 'MailTemplateCategory'
        db.delete_table(u'sendemail_mailtemplatecategory')

        # Deleting model 'MailTemplate'
        db.delete_table(u'sendemail_mailtemplate')


    models = {
        u'sendemail.mailtemplate': {
            'Meta': {'object_name': 'MailTemplate'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sendemail.MailTemplateCategory']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'tag_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'tag_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'sendemail.mailtemplatecategory': {
            'Meta': {'object_name': 'MailTemplateCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['sendemail']