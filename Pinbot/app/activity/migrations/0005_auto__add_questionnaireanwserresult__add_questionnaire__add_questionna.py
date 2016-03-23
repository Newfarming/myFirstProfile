# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'QuestionnaireAnwserResult'
        db.create_table(u'activity_questionnaireanwserresult', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['activity.Questionnaire'])),
            ('anwser', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('questionnaire_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['activity.QuestionnaireResult'])),
        ))
        db.send_create_signal(u'activity', ['QuestionnaireAnwserResult'])

        # Adding model 'Questionnaire'
        db.create_table(u'activity_questionnaire', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('question_type', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('anwser_type', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')()),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('anwser_options', self.gf('django.db.models.fields.CharField')(default='', max_length=300, blank=True)),
        ))
        db.send_create_signal(u'activity', ['Questionnaire'])

        # Adding model 'QuestionnaireResult'
        db.create_table(u'activity_questionnaireresult', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('submit_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'activity', ['QuestionnaireResult'])


    def backwards(self, orm):
        # Deleting model 'QuestionnaireAnwserResult'
        db.delete_table(u'activity_questionnaireanwserresult')

        # Deleting model 'Questionnaire'
        db.delete_table(u'activity_questionnaire')

        # Deleting model 'QuestionnaireResult'
        db.delete_table(u'activity_questionnaireresult')


    models = {
        u'activity.closeeasterrecord': {
            'Meta': {'object_name': 'CloseEasterRecord'},
            'close_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'activity.easteregg': {
            'Meta': {'object_name': 'EasterEgg'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'egg_type': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'price': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'})
        },
        u'activity.eggrecord': {
            'Meta': {'object_name': 'EggRecord'},
            'claim_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'claim_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'egg': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'egg_records'", 'to': u"orm['activity.EasterEgg']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'egg_records'", 'to': u"orm['auth.User']"}),
            'user_need': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'activity.questionnaire': {
            'Meta': {'object_name': 'Questionnaire'},
            'anwser_options': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'blank': 'True'}),
            'anwser_type': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'question_type': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'activity.questionnaireanwserresult': {
            'Meta': {'object_name': 'QuestionnaireAnwserResult'},
            'anwser': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['activity.Questionnaire']"}),
            'questionnaire_page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['activity.QuestionnaireResult']"})
        },
        u'activity.questionnaireresult': {
            'Meta': {'object_name': 'QuestionnaireResult'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'submit_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['activity']