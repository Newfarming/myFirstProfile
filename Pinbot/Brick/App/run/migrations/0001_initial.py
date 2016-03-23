# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DailyReport'
        db.create_table(u'run_dailyreport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('register_user_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_user_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('login_user_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('login_percent', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('reco_job_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('check_job_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('favour_job_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('send_job_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('dislike_job_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('refresh_job_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('favour_company_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('report_date', self.gf('django.db.models.fields.DateField')(db_index=True)),
        ))
        db.send_create_signal(u'run', ['DailyReport'])


    def backwards(self, orm):
        # Deleting model 'DailyReport'
        db.delete_table(u'run_dailyreport')


    models = {
        u'run.dailyreport': {
            'Meta': {'object_name': 'DailyReport'},
            'check_job_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'code_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'dislike_job_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'favour_company_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'favour_job_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login_percent': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'login_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'reco_job_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'refresh_job_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'register_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'report_date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'send_job_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['run']