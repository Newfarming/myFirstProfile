# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'InterviewTermQuestions'
        db.create_table(u'tutorial_interviewtermquestions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('anwser', self.gf('django.db.models.fields.TextField')(max_length=254)),
            ('question_type', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'tutorial', ['InterviewTermQuestions'])

        # Adding model 'FeedBackText'
        db.create_table(u'tutorial_feedbacktext', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feedback_text', self.gf('django.db.models.fields.TextField')(max_length=254)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('feedback_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'tutorial', ['FeedBackText'])


    def backwards(self, orm):
        # Deleting model 'InterviewTermQuestions'
        db.delete_table(u'tutorial_interviewtermquestions')

        # Deleting model 'FeedBackText'
        db.delete_table(u'tutorial_feedbacktext')


    models = {
        u'tutorial.feedbacktext': {
            'Meta': {'object_name': 'FeedBackText'},
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'feedback_text': ('django.db.models.fields.TextField', [], {'max_length': '254'}),
            'feedback_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'tutorial.interviewtermquestions': {
            'Meta': {'object_name': 'InterviewTermQuestions'},
            'anwser': ('django.db.models.fields.TextField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'question_type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['tutorial']