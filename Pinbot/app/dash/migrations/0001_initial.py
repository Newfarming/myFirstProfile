# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ResumeDailyReportData'
        db.create_table(u'dash_resumedailyreportdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resume_commends_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('resume_view_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('resume_down_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('interviewed_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('entered_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('company_card_send_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('report_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'dash', ['ResumeDailyReportData'])

        # Adding model 'UserDailyReportData'
        db.create_table(u'dash_userdailyreportdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pv', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('uv', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('new_register_user_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('new_active_user_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('new_normal_user_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('new_vip_user_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('lively_user_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('repeat_visit_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('week_repeat_visit_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('month_repeat_visit_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_register_user_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_active_user_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_normal_user_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_vip_user_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('report_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'dash', ['UserDailyReportData'])

        # Adding model 'PinbotDailyReport'
        db.create_table(u'dash_pinbotdailyreport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pv', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('uv', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('register_user_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_user_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('login_user_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pay_user_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_pay_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('report_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'dash', ['PinbotDailyReport'])


    def backwards(self, orm):
        # Deleting model 'ResumeDailyReportData'
        db.delete_table(u'dash_resumedailyreportdata')

        # Deleting model 'UserDailyReportData'
        db.delete_table(u'dash_userdailyreportdata')

        # Deleting model 'PinbotDailyReport'
        db.delete_table(u'dash_pinbotdailyreport')


    models = {
        u'dash.pinbotdailyreport': {
            'Meta': {'object_name': 'PinbotDailyReport'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pay_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pv': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'register_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'report_date': ('django.db.models.fields.DateField', [], {}),
            'total_pay_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'uv': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'dash.resumedailyreportdata': {
            'Meta': {'object_name': 'ResumeDailyReportData'},
            'company_card_send_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'entered_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interviewed_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'report_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'resume_commends_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'resume_down_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'resume_view_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'dash.userdailyreportdata': {
            'Meta': {'object_name': 'UserDailyReportData'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lively_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'month_repeat_visit_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'new_active_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'new_normal_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'new_register_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'new_vip_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pv': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'repeat_visit_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'report_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'total_active_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_normal_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_register_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_vip_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'uv': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'week_repeat_visit_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['dash']