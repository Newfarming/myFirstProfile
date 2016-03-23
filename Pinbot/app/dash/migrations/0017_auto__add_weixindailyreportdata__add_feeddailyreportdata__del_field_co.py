# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WeixinDailyReportData'
        db.create_table(u'dash_weixindailyreportdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('new_bind_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('new_reg_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_bind_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('lively_member_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('lively_user_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('feed_notify_send_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('feed_notify_view_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('new_feed_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('new_feed_favours_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'dash', ['WeixinDailyReportData'])

        # Adding model 'FeedDailyReportData'
        db.create_table(u'dash_feeddailyreportdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('lively_feed_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('new_feed_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('lively_feed_user_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('lively_feed_member_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'dash', ['FeedDailyReportData'])

        # Deleting field 'CoreDailyReportData.entered_count'
        db.delete_column(u'dash_coredailyreportdata', 'entered_count')

        # Adding field 'CoreDailyReportData.register_user_count'
        db.add_column(u'dash_coredailyreportdata', 'register_user_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'ResumeDailyReportData.resume_fav_count'
        db.add_column(u'dash_resumedailyreportdata', 'resume_fav_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'UserDailyReportData.total_self_member_c_count'
        db.delete_column(u'dash_userdailyreportdata', 'total_self_member_c_count')

        # Deleting field 'UserDailyReportData.week_repeat_visit_count'
        db.delete_column(u'dash_userdailyreportdata', 'week_repeat_visit_count')

        # Deleting field 'UserDailyReportData.new_self_member_a_count'
        db.delete_column(u'dash_userdailyreportdata', 'new_self_member_a_count')

        # Deleting field 'UserDailyReportData.new_self_member_b_count'
        db.delete_column(u'dash_userdailyreportdata', 'new_self_member_b_count')

        # Deleting field 'UserDailyReportData.total_self_member_b_count'
        db.delete_column(u'dash_userdailyreportdata', 'total_self_member_b_count')

        # Deleting field 'UserDailyReportData.total_self_member_a_count'
        db.delete_column(u'dash_userdailyreportdata', 'total_self_member_a_count')

        # Deleting field 'UserDailyReportData.pv'
        db.delete_column(u'dash_userdailyreportdata', 'pv')

        # Deleting field 'UserDailyReportData.week_lively_user_count'
        db.delete_column(u'dash_userdailyreportdata', 'week_lively_user_count')

        # Deleting field 'UserDailyReportData.new_self_member_c_count'
        db.delete_column(u'dash_userdailyreportdata', 'new_self_member_c_count')

        # Deleting field 'UserDailyReportData.new_active_user_count'
        db.delete_column(u'dash_userdailyreportdata', 'new_active_user_count')

        # Deleting field 'UserDailyReportData.month_lively_user_count'
        db.delete_column(u'dash_userdailyreportdata', 'month_lively_user_count')

        # Deleting field 'UserDailyReportData.uv'
        db.delete_column(u'dash_userdailyreportdata', 'uv')

        # Deleting field 'UserDailyReportData.month_repeat_visit_count'
        db.delete_column(u'dash_userdailyreportdata', 'month_repeat_visit_count')


    def backwards(self, orm):
        # Deleting model 'WeixinDailyReportData'
        db.delete_table(u'dash_weixindailyreportdata')

        # Deleting model 'FeedDailyReportData'
        db.delete_table(u'dash_feeddailyreportdata')

        # Adding field 'CoreDailyReportData.entered_count'
        db.add_column(u'dash_coredailyreportdata', 'entered_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'CoreDailyReportData.register_user_count'
        db.delete_column(u'dash_coredailyreportdata', 'register_user_count')

        # Deleting field 'ResumeDailyReportData.resume_fav_count'
        db.delete_column(u'dash_resumedailyreportdata', 'resume_fav_count')

        # Adding field 'UserDailyReportData.total_self_member_c_count'
        db.add_column(u'dash_userdailyreportdata', 'total_self_member_c_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserDailyReportData.week_repeat_visit_count'
        db.add_column(u'dash_userdailyreportdata', 'week_repeat_visit_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserDailyReportData.new_self_member_a_count'
        db.add_column(u'dash_userdailyreportdata', 'new_self_member_a_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserDailyReportData.new_self_member_b_count'
        db.add_column(u'dash_userdailyreportdata', 'new_self_member_b_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserDailyReportData.total_self_member_b_count'
        db.add_column(u'dash_userdailyreportdata', 'total_self_member_b_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserDailyReportData.total_self_member_a_count'
        db.add_column(u'dash_userdailyreportdata', 'total_self_member_a_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserDailyReportData.pv'
        db.add_column(u'dash_userdailyreportdata', 'pv',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserDailyReportData.week_lively_user_count'
        db.add_column(u'dash_userdailyreportdata', 'week_lively_user_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserDailyReportData.new_self_member_c_count'
        db.add_column(u'dash_userdailyreportdata', 'new_self_member_c_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserDailyReportData.new_active_user_count'
        db.add_column(u'dash_userdailyreportdata', 'new_active_user_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserDailyReportData.month_lively_user_count'
        db.add_column(u'dash_userdailyreportdata', 'month_lively_user_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserDailyReportData.uv'
        db.add_column(u'dash_userdailyreportdata', 'uv',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserDailyReportData.month_repeat_visit_count'
        db.add_column(u'dash_userdailyreportdata', 'month_repeat_visit_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    models = {
        u'dash.coredailyreportdata': {
            'Meta': {'ordering': "['-report_date']", 'object_name': 'CoreDailyReportData'},
            'active_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lively_member_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'lively_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'member_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'register_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'repeat_visit_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'report_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'dash.feeddailyreportdata': {
            'Meta': {'ordering': "['-report_date']", 'object_name': 'FeedDailyReportData'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lively_feed_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'lively_feed_member_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'lively_feed_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'new_feed_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'report_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'dash.partnerdailyreportdata': {
            'Meta': {'ordering': "['-report_date']", 'object_name': 'PartnerDailyReportData'},
            'accept_task_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'accept_task_user_total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'accusation_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'accusation_total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'all_extra_reward_coin_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'all_reward_coin_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'today_extra_reward_coin_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'today_reward_coin_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'resume_fav_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'resume_view_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'dash.userdailyreportdata': {
            'Meta': {'ordering': "['-report_date']", 'object_name': 'UserDailyReportData'},
            'all_total_active_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lively_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'new_experience_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'new_manual_member_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'new_member_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'new_register_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'new_self_member_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'repeat_visit_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'report_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'total_experience_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_manual_member_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_member_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_register_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_self_member_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'dash.weixindailyreportdata': {
            'Meta': {'ordering': "['-report_date']", 'object_name': 'WeixinDailyReportData'},
            'feed_notify_send_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'feed_notify_view_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lively_member_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'lively_user_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'new_bind_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'new_feed_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'new_feed_favours_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'new_reg_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'report_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'total_bind_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['dash']