# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'PartnerDailyReportData.commend_resume_count'
        db.delete_column(u'dash_partnerdailyreportdata', 'commend_resume_count')

        # Deleting field 'PartnerDailyReportData.commend_resume_total_count'
        db.delete_column(u'dash_partnerdailyreportdata', 'commend_resume_total_count')

        # Adding field 'PartnerDailyReportData.upload_resume_count'
        db.add_column(u'dash_partnerdailyreportdata', 'upload_resume_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'PartnerDailyReportData.upload_resume_total_count'
        db.add_column(u'dash_partnerdailyreportdata', 'upload_resume_total_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'PartnerDailyReportData.commend_resume_count'
        db.add_column(u'dash_partnerdailyreportdata', 'commend_resume_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'PartnerDailyReportData.commend_resume_total_count'
        db.add_column(u'dash_partnerdailyreportdata', 'commend_resume_total_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'PartnerDailyReportData.upload_resume_count'
        db.delete_column(u'dash_partnerdailyreportdata', 'upload_resume_count')

        # Deleting field 'PartnerDailyReportData.upload_resume_total_count'
        db.delete_column(u'dash_partnerdailyreportdata', 'upload_resume_total_count')


    models = {
        u'dash.partnerdailyreportdata': {
            'Meta': {'ordering': "['-report_date']", 'object_name': 'PartnerDailyReportData'},
            'accept_task_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'accept_task_user_total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'accusation_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'accusation_total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'do_task_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'do_task_total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'entered_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'entered_total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interviewed_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'interviewed_total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'report_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'resume_download_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'resume_download_total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'resume_viewed_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'resume_viewed_total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'task_accedpted_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'task_accedpted_count_contrast': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'task_accedpted_total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'task_total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'task_viewed_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'today_commend_and_check_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'today_commend_and_download_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'upload_resume_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'upload_resume_total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
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
            'Meta': {'ordering': "['-report_date']", 'object_name': 'ResumeDailyReportData'},
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
            'Meta': {'ordering': "['-report_date']", 'object_name': 'UserDailyReportData'},
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