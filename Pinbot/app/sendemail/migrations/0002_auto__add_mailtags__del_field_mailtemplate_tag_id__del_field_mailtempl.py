# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MailTags'
        db.create_table(u'sendemail_mailtags', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag_id', self.gf('django.db.models.fields.IntegerField')(unique=True, null=True, blank=True)),
            ('tag_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'sendemail', ['MailTags'])

        # Deleting field 'MailTemplate.tag_id'
        db.delete_column(u'sendemail_mailtemplate', 'tag_id')

        # Deleting field 'MailTemplate.tag_name'
        db.delete_column(u'sendemail_mailtemplate', 'tag_name')


    def backwards(self, orm):
        # Deleting model 'MailTags'
        db.delete_table(u'sendemail_mailtags')

        # Adding field 'MailTemplate.tag_id'
        db.add_column(u'sendemail_mailtemplate', 'tag_id',
                      self.gf('django.db.models.fields.IntegerField')(unique=True, null=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'MailTemplate.tag_name'
        raise RuntimeError("Cannot reverse this migration. 'MailTemplate.tag_name' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'MailTemplate.tag_name'
        db.add_column(u'sendemail_mailtemplate', 'tag_name',
                      self.gf('django.db.models.fields.CharField')(max_length=50),
                      keep_default=False)


    models = {
        u'sendemail.mailtags': {
            'Meta': {'object_name': 'MailTags'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'tag_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'sendemail.mailtemplate': {
            'Meta': {'object_name': 'MailTemplate'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sendemail.MailTemplateCategory']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'sendemail.mailtemplatecategory': {
            'Meta': {'object_name': 'MailTemplateCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['sendemail']