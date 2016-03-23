# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserDailyReportData.new_member_count'
        db.add_column(u'dash_userdailyreportdata', 'new_member_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserDailyReportData.total_member_count'
        db.add_column(u'dash_userdailyreportdata', 'total_member_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserDailyReportData.all_total_active_user_count'
        db.add_column(u'dash_userdailyreportdata', 'all_total_active_user_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UserDailyReportData.new_member_count'
        db.delete_column(u'dash_userdailyreportdata', 'new_member_count')

        # Deleting field 'UserDailyReportData.total_member_count'
        db.delete_column(u'dash_userdailyreportdata', 'total_member_count')

        # Deleting field 'UserDailyReportData.all_total_active_user_count'
        db.delete_column(u'dash_userdailyreportdata', 'all_total_active_user_count')


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
            'all_total_active_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lively_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'month_repeat_visit_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'new_active_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'new_member_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'new_normal_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'new_register_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'new_vip_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pv': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'repeat_visit_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'report_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'total_active_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_member_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_normal_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_register_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_vip_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'uv': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'week_repeat_visit_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['dash']