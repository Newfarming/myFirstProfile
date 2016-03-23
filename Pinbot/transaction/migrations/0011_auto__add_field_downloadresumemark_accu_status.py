# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'DownloadResumeMark.accu_status'
        db.add_column(u'transaction_downloadresumemark', 'accu_status',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'DownloadResumeMark.accu_status'
        db.delete_column(u'transaction_downloadresumemark', 'accu_status')


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
            'add_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 5, 7, 0, 0)'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['jobs.CompanyCategory']", 'null': 'True', 'blank': 'True'}),
            'company_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'company_stage': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'core_team': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            'desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'favour_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_points': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'need_recommend': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'pinbot_recommend': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'blank': 'True'}),
            'product_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'jobs.companycategory': {
            'Meta': {'object_name': 'CompanyCategory'},
            'brick_display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'jobs.job': {
            'Meta': {'object_name': 'Job'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 5, 7, 0, 0)'}),
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
            'Meta': {'unique_together': "(('send_user', 'resume_id'),)", 'object_name': 'SendCompanyCard'},
            'download_status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'feed_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'feedback_status': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'feedback_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 5, 7, 0, 0)'}),
            'has_download': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jobs.Job']", 'null': 'True', 'blank': 'True'}),
            'points_used': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'resume_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'send_msg': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'send_status': ('django.db.models.fields.IntegerField', [], {'default': '2', 'null': 'True', 'blank': 'True'}),
            'send_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 5, 7, 0, 0)'}),
            'send_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'to_email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'payment.paymentorder': {
            'Meta': {'object_name': 'PaymentOrder'},
            'actual_price': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'feed_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'feed_price': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'feed_service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pinbot_package.FeedService']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pinbot_package.ResumePackge']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'package_price': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'pay_status': ('django.db.models.fields.CharField', [], {'default': "'unpay'", 'max_length': '20'}),
            'payment_terms': ('django.db.models.fields.CharField', [], {'default': "'alipay'", 'max_length': '20'}),
            'total_price': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'pinbot_package.feedservice': {
            'Meta': {'object_name': 'FeedService'},
            'display': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'feed_num': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'valid_days': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'pinbot_package.resumepackge': {
            'Meta': {'object_name': 'ResumePackge'},
            'actual_resume_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'company_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'feed_service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pinbot_package.FeedService']"}),
            'feed_service_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'feed_service_value': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'resume_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'valid_days': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'system.resumemarksetting': {
            'Meta': {'object_name': 'ResumeMarkSetting'},
            'change': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'classify': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'end_status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'good_result': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'has_interview': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_accu': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'transaction.adminmarklog': {
            'Meta': {'object_name': 'AdminMarkLog'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'resume_mark': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'admin_logs'", 'to': u"orm['transaction.DownloadResumeMark']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'transaction.downloadresumemark': {
            'Meta': {'object_name': 'DownloadResumeMark'},
            'accu_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'buy_record': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'resume_mark'", 'unique': 'True', 'to': u"orm['transaction.ResumeBuyRecord']"}),
            'current_mark': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'current_marks'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['system.ResumeMarkSetting']"}),
            'has_interview': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_mark': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'last_marks'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['system.ResumeMarkSetting']"}),
            'mark_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pay_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'verify_status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'transaction.feedbackinfo': {
            'Meta': {'object_name': 'FeedBackInfo'},
            'feedback_desc': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'feedback_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transaction.FeedBackType']"})
        },
        u'transaction.feedbacktype': {
            'Meta': {'object_name': 'FeedBackType'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            're_points': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'transaction.resumebuyrecord': {
            'Meta': {'object_name': 'ResumeBuyRecord'},
            'feed_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'feedback_info': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transaction.FeedBackInfo']", 'null': 'True', 'blank': 'True'}),
            'finished_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 1, 0, 0)', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'op_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'resume_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'resume_url': ('django.db.models.fields.URLField', [], {'max_length': '1000'}),
            'send_card': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jobs.SendCompanyCard']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'transaction.userchargepackage': {
            'Meta': {'object_name': 'UserChargePackage'},
            'actual_cost': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'extra_feed_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'feed_end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 5, 6, 0, 0)', 'db_index': 'True'}),
            'feed_package': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pinbot_package.FeedService']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['payment.PaymentOrder']", 'null': 'True', 'blank': 'True'}),
            'package_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pay_status': ('django.db.models.fields.CharField', [], {'default': "'Start'", 'max_length': '50'}),
            'pkg_source': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            're_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rest_feed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rest_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'resume_end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 5, 6, 0, 0)', 'db_index': 'True'}),
            'resume_package': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pinbot_package.ResumePackge']", 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 5, 7, 0, 0)'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'zero_points_notify_status': ('django.db.models.fields.CharField', [], {'default': "'read'", 'max_length': '50'})
        },
        u'transaction.usermarklog': {
            'Meta': {'object_name': 'UserMarkLog'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mark': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mark_logs'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['system.ResumeMarkSetting']"}),
            'mark_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'resume_mark': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mark_logs'", 'to': u"orm['transaction.DownloadResumeMark']"})
        },
        u'transaction.userresumefeedback': {
            'Meta': {'object_name': 'UserResumeFeedback'},
            'check_comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'check_status': ('django.db.models.fields.CharField', [], {'default': "'checking'", 'max_length': '50'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 5, 7, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'feedback_info': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transaction.FeedBackInfo']"}),
            'feedback_value': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notify_status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'resume_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['transaction']