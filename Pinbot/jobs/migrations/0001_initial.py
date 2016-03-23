# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Company'
        db.create_table(u'jobs_company', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company_name', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('key_points', self.gf('django.db.models.fields.CharField')(default='', max_length=1000, null=True, blank=True)),
            ('desc', self.gf('django.db.models.fields.CharField')(default='', max_length=1000, null=True, blank=True)),
            ('core_team', self.gf('django.db.models.fields.CharField')(default='', max_length=1000, null=True, blank=True)),
            ('company_stage', self.gf('django.db.models.fields.CharField')(default='', max_length=1000, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('product_url', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('add_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 1, 5, 0, 0))),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'jobs', ['Company'])

        # Adding model 'Job'
        db.create_table(u'jobs_job', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('salary_low', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('salary_high', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('work_years', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('address', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('degree', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('key_points', self.gf('django.db.models.fields.CharField')(default='', max_length=1000, null=True, blank=True)),
            ('desc', self.gf('django.db.models.fields.CharField')(default='', max_length=1000, null=True, blank=True)),
            ('skill_desc', self.gf('django.db.models.fields.CharField')(default='', max_length=1000, null=True, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jobs.Company'])),
            ('add_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 1, 5, 0, 0))),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'jobs', ['Job'])

        # Adding model 'HunterInterest'
        db.create_table(u'jobs_hunterinterest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.CharField')(default='', max_length=1000)),
            ('interest_type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jobs.Company'], null=True, blank=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jobs.Job'], null=True, blank=True)),
            ('is_interest', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('add_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 1, 5, 0, 0))),
            ('click', self.gf('django.db.models.fields.IntegerField')(default=1, null=True, blank=True)),
            ('ip', self.gf('django.db.models.fields.CharField')(default='', max_length=200, null=True, blank=True)),
            ('access_url', self.gf('django.db.models.fields.CharField')(default='', max_length=200, null=True, blank=True)),
            ('refer_url', self.gf('django.db.models.fields.CharField')(default='', max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'jobs', ['HunterInterest'])

        # Adding model 'SendCompanyCard'
        db.create_table(u'jobs_sendcompanycard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('send_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('resume_id', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('has_download', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('download_status', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('to_email', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('send_status', self.gf('django.db.models.fields.IntegerField')(default=2, null=True, blank=True)),
            ('send_msg', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True, blank=True)),
            ('send_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 1, 5, 0, 0))),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jobs.Job'], null=True, blank=True)),
            ('feedback_status', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('feedback_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 1, 5, 0, 0))),
            ('points_used', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal(u'jobs', ['SendCompanyCard'])


    def backwards(self, orm):
        # Deleting model 'Company'
        db.delete_table(u'jobs_company')

        # Deleting model 'Job'
        db.delete_table(u'jobs_job')

        # Deleting model 'HunterInterest'
        db.delete_table(u'jobs_hunterinterest')

        # Deleting model 'SendCompanyCard'
        db.delete_table(u'jobs_sendcompanycard')


    models = {
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
        },
        u'jobs.company': {
            'Meta': {'object_name': 'Company'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 1, 5, 0, 0)'}),
            'company_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'company_stage': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'core_team': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_points': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'product_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'jobs.hunterinterest': {
            'Meta': {'object_name': 'HunterInterest'},
            'access_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'add_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 1, 5, 0, 0)'}),
            'click': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jobs.Company']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'ip': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'is_interest': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jobs.Job']", 'null': 'True', 'blank': 'True'}),
            'refer_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'})
        },
        u'jobs.job': {
            'Meta': {'object_name': 'Job'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 1, 5, 0, 0)'}),
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jobs.Company']"}),
            'degree': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_points': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'salary_high': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'salary_low': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'skill_desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'work_years': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'jobs.sendcompanycard': {
            'Meta': {'object_name': 'SendCompanyCard'},
            'download_status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'feedback_status': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'feedback_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 1, 5, 0, 0)'}),
            'has_download': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jobs.Job']", 'null': 'True', 'blank': 'True'}),
            'points_used': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'resume_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'send_msg': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'send_status': ('django.db.models.fields.IntegerField', [], {'default': '2', 'null': 'True', 'blank': 'True'}),
            'send_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 1, 5, 0, 0)'}),
            'send_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'to_email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['jobs']